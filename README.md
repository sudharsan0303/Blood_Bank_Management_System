## Overview:
The Blood Bank Management System is a web application designed to help blood banks manage donor information, donation records, and blood requests efficiently. This system is built using Flask, SQLite, and other modern web technologies such as HTML and CSS for the frontend. It provides a secure and easy-to-use platform for donors to register, donate blood, and track their donation history.

## Features
1. User Registration & Login
2. Forgot Password (Reset using username or email, without sending mail)
3. Blood Donation Management
4. User Donation History

## Installation

1. Install Python:
   - Download and install Python from [Python.org](https://www.python.org/?downloads)
2. Download the Source Code:
   - Download the source code and extract it.
3. Open the Project:
   - Open the folder containing the source code in VS Code.
5. Step-by-step Command Line Installation in VS Code:
    1. Install Flask:
       - Run the command: `pip install Flask`
    2. Install Werkzeug:
       - Run the command: `pip install Werkzeug`
    3. SQLite3
       - SQLite is included with Python's standard library, so you usually don't need to install it separately.
    4. Install Flask-SQLAlchemy:
       - Run the command: `pip install Flask-SQLAlchemy`
    5. Install Flask-CORS:
       - Run the command: `pip install Flask-CORS`
6. All-in-One Command Line Installation VS code:
   - Run the command: `pip install Flask Werkzeug Flask-SQLAlchemy Flask-CORS`

## Running the Application:
1. Check the database files (`user_data.db`, `donar_data.db`, `request_data.db`) located in the `data` folder.
   - if `user_data.db` is missing, then run `setup_user_database.py` file to create a user database.
   - if `donar_data.db` is missing, then run  `setup_donar_database.py` file to create a donar database.
   - if `request_data.db` is missing, then run `setup_request_database.py` file to create a request database.
2. Open the Command Line in VS Code.
3. Run the application with the following command: `python app.py`
4. Or, right-click the app.py file and select Run in Terminal.
