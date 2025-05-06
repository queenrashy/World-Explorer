-- signup --
**Endpoint**:
	/signup

**Method**: 
	POST

**Description**: 
	Create a new account with full name, email, phone number, and password.  Sends a welcome email after successful registration.

**Request body**:
```
	{
	"fullName": "Adebisi Queen",
	"email": "adebisiqueen231@gmail.com",
	"phone": "08139704781",
	"password": "12345678"
	}
```

**Validation Rules**:
	fullName: required, minimum 2 characters.
	email: required, must be a valid email format, must be unique.
	phone: optional(if you're not validating it).
	password: required, minimum 8 characters.

**Response**:
```
	{
	"message": "Account created and email sent successfully.",
	"success": true"
	}
```

Status code: 200 Ok

**Error Responses**:

| Secnario                      | Status Code | Error Message(JSON)                                    |
| ----------------------------- | ----------- | ------------------------------------------------------ |
| Missing or short name         | 400         | Please enter a valid name!                             |
| Invalid email format          | 400         | Please enter a valid email address                     |
| Email already exists          | 400         | Email already exists                                   |
| Weak or missing password      | 400         | Password is Invalid, please enter 8 or more characters |
| other internal errors(e.g DB) | 400         | User signup error: <error message>                     |

%% login %%
**Endpoint**:
	/login

**Method**:
	GET

**Description**:
	log in with email and password. Returns JWT token on successful login and deletes any previously stored token.

**Request body**:
json:
```
{
	"email": "adebisiqueen231@gmail.com",
	"password": "1234567"
}
```

**Validation Rules**:
1. ==email==: required, must be valid email format, must already exists in the database.
2. ==password==: required, must match the user's saved password.

**Response**:
json:
```
{
"success": True,
"token": "Jwt_token_here"
}
```

Status code: 200 Ok

**Error Response**:

| Scenario                  | Status Code | Error Message                          |
| ------------------------- | ----------- | -------------------------------------- |
| Missing email or password | 400         | Please enter a valid email or password |
| Invalid email format      | 400         | Please enter a valid email address     |
| Email not found           | 401         | User with this email does not exist    |
| Incorrect password        | 400         | Invalid email or password              |

%% logout %%
**Endpoint**:
	/logout

**Method**:
	GET

**Description**:
	Log out the currently authenticated user. Deletes the active JWT token and sends a logout confirmation email to the user's registration email address.

**Authentication**:
	This routes requires a valid JWT token via `@auth.login_required`.


**Request body**:
	No request body required. The JWT token must be sent in the headers for authentication.

Response:
json:
```
{
	"success": true,
	"message": "User logout successfully"
}
```

Error Responses:

| Scenario              | Status Code | Error Message(JSON)                         |
| --------------------- | ----------- | ------------------------------------------- |
| Missing/Invalid Token | 401         | Authentication required or token is invalid |

%% forget password %%
**Endpoint**:
	/forget-password

**Methods**:
	POST

**Description**:
	Initiates the password reset process by generating a unique token and sending it to the user's registered email address.

**Request Body**:
json:
```
{
"email": "adebisiqueen@gmail.com"
}
```

**Validation Rules**:
	==email==: required, must be a valid email format, and must exist in the database.

**Response**:
json:
```
{
"success": true,
"message": "Password reset email sent"
}
```
Status code: 200 ok

**Error Response**:

| Scenario             | Status Code | Error Message                       |
| -------------------- | ----------- | ----------------------------------- |
| Missing email        | 400         | Please enter email                  |
| Email not registered | 400         | User with this email does not exist |

%% reset password %%
**Endpoint**:
	/reset-password

**Method**:
	POST

**Description**:
	Allows users to reset their password using a valid reset token sent to their email.

Request Body:
json:
```
{
"token": "ADKDF34MCM",
"new_password" "Queen33tti"
"comfirm_password" "Queen33tti"
}
```

Validation Rules:
1. ==token==: required, must exist in database, must not be previously used.
2. ==new_password==: reuqired, must match ==comfirm_password==, minimum 8 characters (if enforced).
3. ==confirm_password==: must match ==new_password==.

**Response**:
json:
```
{
"success": true,
"message": "Password reset successfully"
}
```
Status Code: 200 OK

**Error Responses:**

| Scenario                       | Status Code | Error Message(JSON)         |
| ------------------------------ | ----------- | --------------------------- |
| Missing or mismatched password | 400         | Password does not match     |
| Missing token                  | 400         | Please enter token          |
| Invalid token                  | 400         | Invalid token               |
| Token already used             | 400         | Token has been used already |
| User not found                 | 400         | User not found              |

%% delete account %%
**Endpoint**:
	/<int:did>

**Methods**:
	DELETE

**Authentication Required:**
	Yes- JWT Via ==token==

Description:
	Deletes a user account by ID if it exist. Returns confirmation upon successful deletion.

**Path Parameter**:

| Parameter | Type | Description              |
| --------- | ---- | ------------------------ |
| did       | int  | ID of the user to delete |

**Success Response**:
```
{
"done": true,
"message": "adebisiqueen@gmail.com Account deleted successfully!"
}
```

**Error Response**:

| Scenario            | Status Code | Error Message(JSON) |
| ------------------- | ----------- | ------------------- |
| User does not exist | 404         | User does not exist |
%% list of countries %%
**Endpoint**:
	/countries

**Method**:
	POST

**Authentication Required:**
	Yes- JWT Via ==@auth.login_required==

**Description**:
	Returns a list of all countries. if a search query is provided, it filters the countries that match the query (case-insensitive).

**Request Body**:
json:
```
{
"query": "united"
}
```
The query filed is optional. if omitted, it returns all countries

**Response**:
json:
```
{
"countries": 
    "United Arab Emirates",
    "United Kingdom",
    "United States"
}
```

**Status Code**: 200 OK

**Error Response**:


| Scenario                | Status Code | Error Message(Json)                 |
| ----------------------- | ----------- | ----------------------------------- |
| REST API fails to fetch | 500         | Failed to fetch country list        |
| Unauthorized access     | 401         | Unauthorized- Token missing/invalid |


%% get country information %%
**Endpoint**:
	/country-info

**Method**:
	POST

**Authentication Required**:
	Yes -JWT ==Token==

**Description**:
	Search and returns detailed information about a specific country using the **REST Countries API**. Saves the search term to the user's history.

**Request Body**:
json:
```
{
"country": "nigeria"
}
```

**Validation Rules**:
1. ==country==: required, must be a valid country name string.

**Response**:
json:
```
{
  "result": [
    {
      "name": "Nigeria",
      "capital": "Abuja",
      "region": "Africa",
      "callingCode": "+234",
      "subregion": "Western Africa",
      "population": 206139589,
      "flag": "https://flagcdn.com/w320/ng.png",
      "languages": ["English"],
      "timezones": ["UTC+01:00"],
      "latlng": [10, 8],
      "currencies": ["NGN"]
    }
  ]
}
```
**Status Code**: 200 OK

**Error Response**:

| Scenario                     | Status Code | Error Message (JSON)                 |
| ---------------------------- | ----------- | ------------------------------------ |
| Missing country field        | 400         | Please provide a country name        |
| Country not found or invalid | 400         | Country not found                    |
| Unauthorized access          | 401         | Unauthorized -Token missing/invalid  |

%% search capital %%
**Endpoint**:
	/city

**Method**:
	POST

**Authentication Required**:
	Yes- JWT ==Token==

**Description**:
	Fetches information about a country based on the capital city name using the ==REST Countries Api==. Also Saves the capital search to the user's search history with type "city".

**Request Body**:
json:
```
{
"capital": "abuja"
}
```

**Validation Rules**:
1. ==capital==: required, must be a valid capital city name string.

**Response**:
json:
```
[
  {
    "name": {
      "common": "Nigeria",
      "official": "Federal Republic of Nigeria",
      "nativeName": {
        "eng": {
          "common": "Nigeria",
          "official": "Federal Republic of Nigeria"
        }
      }
    },
    "capital": ["Abuja"],
    "region": "Africa",
    "subregion": "Western Africa",
    "population": 206139587,
    "area": 923768.0,
    "languages": {
      "eng": "English"
    },
    "timezones": ["UTC+01:00"],
    "latlng": [10.0, 8.0],
    "flag": "🇳🇬",
    "flags": {
      "png": "https://flagcdn.com/w320/ng.png",
      "svg": "https://flagcdn.com/ng.svg",
      "alt": "The flag of Nigeria is composed of three equal vertical bands of green, white and green."
    },
    "currencies": {
      "NGN": {
        "name": "Nigerian naira",
        "symbol": "₦"
      }
    },
    "idd": {
      "root": "+2",
      "suffixes": ["34"]
    },
    "maps": {
      "googleMaps": "https://goo.gl/maps/LTn417qWwBPFszuV9",
      "openStreetMaps": "https://www.openstreetmap.org/relation/192787"
    },
    "coatOfArms": {
      "png": "https://mainfacts.com/media/images/coats_of_arms/ng.png",
      "svg": "https://mainfacts.com/media/images/coats_of_arms/ng.svg"
    },
    "tld": [".ng"],
    "translations": {
      "spa": {
        "common": "Nigeria",
        "official": "República Federal de Nigeria"
      },
      "zho": {
        "common": "尼日利亚",
        "official": "尼日利亚联邦共和国"
      }
      // and many more...
    }
  }
]
```

**Error Response**:

| Error Message (Json)                 | Scenario                     | Status Code |
| ------------------------------------ | ---------------------------- | ----------- |
| Please provide a capital             | Capital not provided         | 400         |
| Error fetching data: <error_message> | External API request failure | 500         |
| Unauthorized- Token missing/invalid  | Unauthorized acess           | 401         |

%% retrieve user history %%
**Endpoint**:
	/search-history

**Methods**:
	GET

**Description**:
	Returns the authentication user's past searches, including the search term, type, and the timestamp of each search. The result are sorted from newest to oldest.

**Header**:
	==Authorization: Bearer <your_token>==

**Request Body**:
	None (this is a GET request)


**Success Response**:
json:
```
{
  "history": [
    {
      "searchTerm": "Abuja",
      "searchType": "city",
      "timestamp": "2025-05-05 13:42:10"
    },
    {
      "searchTerm": "Nigeria",
      "searchType": "country",
      "timestamp": "2025-05-04 18:25:34"
    }
    // more results...
  ]
}

```
**Status Code**: 200 OK

**Error Responses**:

| Scenario              | Status Code | Error Message(Json)          |
| --------------------- | ----------- | ---------------------------- |
| Unauthorized request  | 401         | Unauthorized                 |
| Internal server error | 500         | An unexpected error occurred |

%%delete user history  %%
**Endpoint**:
	/history/<int:id>

**Method**:
	DELETE

**Header**:
	==Authorization: Bearer <your_token>==

**Description**:
	Deletes a single search history entry belonging to the authenticated user.

**URL Parameter**:

| Parameter | Type | Required | Description                     |     |
| --------- | ---- | -------- | ------------------------------- | --- |
| id        | int  | Yes      | ID of the search history record |     |

**Request Example**:
```
	DELETE /history/12 HTTP/1.1
	Host: yourapi.com
	Authorization: Bearer <your_token>

```

**Response Body**:
json:
```
{
  "done": true,
  "message": "Search deleted successfully"
}

```
**Status Code** : 200 OK

**Error Response**:

| Scenario                              | Status Code | Error Message(Json)                   |
| ------------------------------------- | ----------- | ------------------------------------- |
| No matching history or not user-owned | 404         | No such history or unauthorized acess |
| Unauthorized                          | 401         | Unauthorized                          |


%%clear all user history  %%
**Endpoint**:
	/history

**Method**:
	DELETE

**Header**:
	==Authorization: Bearer <your_token>==

**Description**:
	Deletes all search history records for the currently authenticated user.

**Request Example**:
```
	DELETE /history HTTP/1.1
	Host: yourapi.com
	Authorization: Bearer <your_token>
```

**Respond Body**:
```
{
  "done": true,
  "message": "All search history deleted successfully"
}

```
**Status Code**: 200 Ok

**Error Response**:

| Scenario                 | Status Code | Error Message (Json)              |
| ------------------------ | ----------- | --------------------------------- |
| No history records found | 404         | No search history found to delete |
| Unauthorized             | 401         | Unauthorized                      |
