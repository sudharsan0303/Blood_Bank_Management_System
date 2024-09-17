from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

# Secret key for session management and flashing messages
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('D:/Program files/PYTHON/flask/Blood_Bank/data/user_data.db')
    conn.row_factory = sqlite3.Row  # This helps to access columns by name
    return conn

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for admin login page
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

# Route for user login page
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query the database to check if the user exists
        cursor.execute('''
            SELECT * FROM users WHERE username = ?
        ''', (username,))

        user = cursor.fetchone()  # Fetch one record
        conn.close()

        if user and check_password_hash(user['password'], password):  # Use check_password_hash
            # If the user exists and the password matches, log them in
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            flash('Login successful!', 'success')  # Flash success message
            return redirect(url_for('user_dashboard'))  # Redirect to dashboard
        else:
            flash('Invalid username or password. Please try again.', 'error')  # Flash error message
            return redirect(url_for('user_login'))  # Stay on the login page

    return render_template('login_page.html')

# Route for create account page
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = int(request.form['age'])
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        blood_type = request.form['blood_type']
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Debug: Check values before insertion
        print(f"Inserting: {full_name}, {age}, {email}, {phone}, {city}, {blood_type}, {username}, {hashed_password}")

        try:
            cursor.execute('''
                INSERT INTO users (full_name, age, email, phone, city, blood_type, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (full_name, age, email, phone, city, blood_type, username, hashed_password))

            conn.commit()
            flash('Account created successfully!')
            return redirect(url_for('user_login'))

        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another.')

        finally:
            conn.close()

    return render_template('create_account.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' in session:
        username = session['username']
        print(f"User {username} accessed the dashboard.")  # Debugging log
        return render_template('dashboard.html', username=username)
    else:
        print("User is not logged in, redirecting to login.")  # Debugging log
        return redirect(url_for('user_login'))  # Redirect to login if not logged in


# Route for contact us page
@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(debug=True)
