import sqlite3


# Connect to the donor_data.db database (it will be created if it doesn't exist)
conn = sqlite3.connect('data/donar_data.db')
cursor = conn.cursor()

    # SQL to create the blood_donations table
cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donar_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            disease TEXT,
            blood_type TEXT NOT NULL,
            date TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            donation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Commit changes and close the connection
conn.commit()
conn.close()
print("Blood Donations table created successfully.")

