import sqlite3

# Connect to the request_data.db database (it will be created if it doesn't exist)
conn = sqlite3.connect('data/request_data.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL statement to create the blood_requests table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blood_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        phone TEXT NOT NULL,
        hospital TEXT NOT NULL,
        city TEXT NOT NULL,
        blood_type TEXT NOT NULL,
        units INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
