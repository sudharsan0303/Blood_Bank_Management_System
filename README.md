## Overview:
The Blood Bank Management System is a web application designed to help blood banks manage donor information, donation records, and blood requests efficiently. This system is built using Flask, SQLite, and other modern web technologies such as HTML and CSS for the frontend. It provides a secure and easy-to-use platform for donors to register, donate blood, and track their donation history.

## Installation

1. Install Python:
   - Download and install Python from [Python.org](https://www.python.org/?downloads)
2. Download the Source Code:
   - Download the source code and extract it.
3. Open the Project:
   - Open the folder containing the source code in VS Code.
5. Install Required Dependencies:
    - Open the command line or terminal within VS Code and run the following command: `pip install -r requirements.txt`

## Running the Application:
1. Check the database files (`user_data.db`, `donar_data.db`, `request_data.db`) located in the `data` folder.
   - if `user_data.db` is missing, then run `setup_user_database.py` file to create a user database.
   - if `donar_data.db` is missing, then run  `setup_donar_database.py` file to create a donar database.
   - if `request_data.db` is missing, then run `setup_request_database.py` file to create a request database.

## Start the Application:

1. Open the command line or terminal in VS Code.
2. Run the following command to start the application: `python app.py`
3. Alternatively, right-click on the `app.py` file in VS Code and select Run in Terminal.

## Access the Application:
1. The application will be accessible at `http://127.0.0.1:5000`.
2. Press Ctrl + click on the link to open it in your browser.
