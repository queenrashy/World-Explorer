import os
from flask import jsonify, request
import requests
from app import app, db
from datetime import datetime
from models import User, PasswordResetToken, StoredjwtToken, SearchHistory
from toolz import random_generator, is_valid_email, send_email
from auth import auth


# user signUp
@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    fullName = data.get('fullName')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    
    # len of name and value input
    if fullName is None or len(fullName) < 2:
        return jsonify({'error': 'Please enter a valid name!'}), 400
    
    # if email valid
    if not is_valid_email(email):
        return jsonify({'error': 'Please enter a valid email address'}), 400
    
    # check unique email
    email_exist = User.query.filter(User.email == email).first()
    if email_exist is not None:
        return jsonify({'error': 'Email already exists'}), 400
    
    # strong password
    if password is None or len(password) < 8:
        return jsonify({'error': 'Password is invalid, please enter 8 or more characters'})
    
    # Create new user account
    new_user = User(fullName=fullName, email=email, phone=phone)
    db.session.add(new_user)
    new_user.set_password(password)
    
    try:
        db.session.commit()
        
        # send email successfully
        subject = 'Welcome to World Explorer'
        text_body = f'hello {fullName},\n\n'
        html_body =f'<h3> {fullName}, </h3> <p>You are now a user. You can explorer and know more about continent or countries </p>'
        
        send_email(subject=subject, receiver=email, text_body=text_body, html_body=html_body)
        
        return jsonify({'success': True, 'message': 'Account created and email sent successfully.'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'User signup error: {e}'}), 400



# User login
@app.route('/login', methods=['GET'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    # validate input
    if email is None or password is None:
        return jsonify({'error': 'Please enter a valid email or password'}), 400
    
    # validate email
    if not is_valid_email(email):
        return jsonify({'error': 'Please enter a valid email address'}), 400
    
    # find user
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'error': 'User with this email does not exist'}), 401
    
    # validate password
    if user.check_password(password):
        # delete previous token
        saved_token = StoredjwtToken.query.filter_by(user_id = user.id).first()
        if saved_token is not None:
            db.session.delete(saved_token)
            
        # password is correct, generate jwt token
        token = user.generate_auth_token()
        new_jwt_token = StoredjwtToken(user_id=user.id, jwt_token=token)
        db.session.add(new_jwt_token)
        db.session.commit()
        return jsonify({'success': True, 'token': token}), 200
    return jsonify({'error': 'Invalid email or password.'}), 400
    
    
# User logout
@app.route('/logout', methods=['GET'])
@auth.login_required 
def logout():
    user = auth.current_user()
    user_id = user.id
    active_token = StoredjwtToken.query.filter_by(user_id=user_id).first()
    db.session.delete(active_token)
    db.session.commit()
    
    # send logout email
    subject = 'Logout Notification'
    text_body = f'Hi {user.fullName}, \n\nYou have successfully logged out of your account.'
    html_body = f" <h3> Hello {user.fullName}, </h3> <p> You have just <strong> logged out </strong> of your account. <p> if this wasn't you, please log in and change your password immediately. </p>"
    
    send_email(subject=subject, receiver=user.email, text_body=text_body, html_body=html_body)
    
    return jsonify({'success': True, 'message': 'User logout successfully'})
     
     
# forget password
@app.route('/forget-password', methods=['POST'])
def forget_password():
    email = request.json.get('email')
    
    # if email exist
    if email is None:
        return jsonify({'error': 'Please enter email'}), 400
    
    user = User.query.filter_by(email=email). first()
    if user is None:
        return jsonify({'error': 'User with this email does not exist'}), 400
    
    # create a password reset token
    token = random_generator(8)
    reset = PasswordResetToken(token=token, user_id=user.id, used=False) 
    db.session.add(reset)
    db.session.commit()
    
    # send password reset token to email
    return jsonify({'success': True, 'message': 'Password reset email sent'}), 200 

# reset password
@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.json.get('token')
    new_password = request.json.get('new_password')
    confirm_password = request.json.get('confirm_password')
    
    if new_password is None or confirm_password != new_password:
        return jsonify({'error': 'Password does not match'}), 400
    
    if token is None:
        return jsonify({'error': 'Please enter token'}), 400
    
    reset = PasswordResetToken.query.filter_by(token=token).first()
    
    if reset is None:
        return jsonify({'error': 'Invalid token'}), 400
    
    if reset.used:
        return jsonify({'error': 'Token has been used already'}), 400
    
    user = User.query.filter_by(id=reset.user_id).first()
    
    if user is None:
        return jsonify({'error': 'User not found'}), 400
    
    user.set_password(new_password)
    reset.used = True
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Password reset successfully'}), 200
    
   
# delete user account  
@app.route('/<int:did>', methods=['DELETE'])
@auth.login_required
def delete_user(did):
    # user = auth.current_user()
    user = User.query.filter(User.id == did).first()
    if user is None:
        return jsonify({'error': 'User does not exit'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'done': True, 'message': f'{user.email } Account deleted successfully!'}) 

# get list of all countries/ or search a country 
@app.route('/countries', methods=['POST'])
@auth.login_required 
def get_country_list():
    query = request.json.get('query') 
    print(f'Searching for countries matching: {query}')
    
    url = 'https://restcountries.com/v3.1/all'
    response = requests.get(url)
    data = response.json()
    
    # Extract all country names
    countries = [country['name']['common'] for country in data]
    
    # filter if a query was provided
    if query:
        query = query.lower()
        countries = [name for name in countries if query in name.lower()]
        
    return jsonify({'countries': sorted(countries)}), 200


# get country info
@app.route('/country-info', methods=['POST'])
@auth.login_required 
def get_country_info():
    user = auth.current_user()
    country_name = request.json.get('country')
    if not country_name:
        return jsonify({'error': 'Please provide a country name'}), 400
    
    # save to history
    history = SearchHistory(user_id=user.id, searchTerm=country_name, searchType='country' )
    db.session.add(history)
    db.session.commit()
    
    url = f'https://restcountries.com/v3.1/name/{country_name}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Country not found'}), 400
    
    data = response.json()
    
    # Simplify and return only key details
    country_data = []
    for country in data:
        country_data.append({
            'name': country['name']['common'],
            'capital': country.get('capital', ['N/A'])[0],
            'region': country.get('region', 'N/A'),
            'callingCode': country.get('idd', {}).get('root', '') + (country.get('idd', {}).get('suffixes', [''])[0]),
            'subregion': country.get('subregion', 'N/A'),
            'population': country.get('population', 'N/A'),
            'flag': country['flags']['png'],
            'languages': list(country.get('languages', {}).values()),
            'timezones': country.get('timezones', []),
            'latlng': country.get('latlng', []),
            'currencies': list(country.get('currencies', {}).keys())
            })
    return jsonify({'result': country_data}), 200


# search capital
@app.route('/city', methods=['POST'])
@auth.login_required 
def get_city():
    user = auth.current_user()
    capital = request.json.get('capital')
    if not capital:
        return jsonify({'error': 'Please provide a capital city name'}), 400
        
    print(f'searching {capital}')
    url = f"https://restcountries.com/v3.1/capital/{capital}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() #raise error if not 200
        data = response.json()
        
        # save to search history
        history = SearchHistory(user_id=user.id, searchTerm=capital, searchType='city')
        db.session.add(history)
        db.session.commit()
        
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500
    
# User retrieve history
@app.route('/search-history', methods=['GET'])
@auth.login_required 
def get_search_history():
    user = auth.current_user()
    history = SearchHistory.query.filter_by(user_id=user.id).order_by(SearchHistory.timestamp.desc()).all()
    
    result = [{
        'searchTerm': item.searchTerm,
        'searchType': item.searchType,
        'timestamp': item.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for item in history]
    
    return jsonify({'history': result}), 200


# user delete history
@app.route('/history/<int:id>', methods=['DELETE'])
@auth.login_required 
def delete_history(id):
    user = auth.current_user()
    history = SearchHistory.query.filter_by(id=id, user_id = user.id).first()
    if history is None:
        return jsonify({'error': 'No such history or unauthorized access'}), 404
    db.session.delete(history)
    db.session.commit()
    return jsonify({'done': True, 'message': 'Search deleted successfully '})
    
    
# user can clear all history
@app.route('/history', methods=['DELETE'])
@auth.login_required 
def delete_all_history():
    user = auth.current_user()
    
    # fetch all search records for the user
    histories = SearchHistory.query.filter_by(user_id=user.id).all()
    
    if not histories:
        return jsonify({'messages': 'No search history found to delete'}), 404
    
    for history in histories:
        db.session.delete(history)
        
    db.session.commit()
    
    return jsonify({'done': True, 'message': 'All search history deleted successfully'})


