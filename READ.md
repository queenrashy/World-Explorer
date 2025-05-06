Flag Explorer is a backend application built with Python, Flask, and SQLAlchemy, designed to serve data about countries and their flags.
The backend integrates with the REST Countries API to fetch and process country metadata such as flag images, capital cities, regions, and populations.
The project exposes clean and well-documented RESTful endpoints that can be consumed by any frontend or client. 
Country data is fetched, normalized, and stored using SQLAlchemy, enabling efficient querying, filtering, and search operations.

[Read docs at](doc.md).

Tech Stack:
- Python 3.x
- Flask (RESTful routing)
- SQLAlchemy (ORM for data modeling and querying)
- REST Countries API (external data source)

Features:
- Integration with external API for real-time data fetching
- RESTful endpoints for accessing country and flag data
- Search and filter support via query parameters
- Modular and maintainable backend architecture
- JSON responses suitable for frontend or mobile consumption
