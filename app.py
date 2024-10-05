from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from datetime import timedelta
from datetime import datetime

app = Flask(__name__)

# Secret key for session management (using environment variable for security)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Set session lifetime (optional for added security)
app.permanent_session_lifetime = timedelta(minutes=30)

# Helper function to get a connection to the users database
def get_db_connection():
    conn = sqlite3.connect('data/user_data.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# Helper function to get a connection to the request data database
def get_request_db_connection():
    conn = sqlite3.connect('data/request_data.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# Helper function to get a connection to the donar data database
def get_donor_db_connection():
    conn = sqlite3.connect('data/donar_data.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# Decorator to protect routes that require user login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function

# Corrected Decorator to protect routes that require admin login
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in as an admin to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to Hash Password
def hash_password(password):
    return generate_password_hash(password)

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for admin login page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password match admin credentials (using environment variables)
        admin_username = os.getenv('ADMIN_USERNAME', 'Adminbloodbank')
        admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@2024bloodbank')

        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True  # Set admin session
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin username or password. Please try again.', 'error')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

# Route for admin logout
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Route for user login page
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Query the database to check if the user exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True  # Make session permanent (optional for session lifetime)
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('user_login'))

    return render_template('login_page.html')

# Route for user logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Route for creating a new account
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

        # Password hash for security
        hashed_password = generate_password_hash(password)

        # Age validation (must be 18 or older)
        if age < 18:
            flash('You must be 18 years or older to create an account.', 'error')
            return redirect(url_for('create_account'))

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (full_name, age, email, phone, city, blood_type, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (full_name, age, email, phone, city, blood_type, username, hashed_password))

            conn.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('user_login'))

        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another.', 'error')

        finally:
            conn.close()

    return render_template('create_account.html')

# Protected route for user dashboard
@app.route('/user_dashboard')
@login_required
def user_dashboard():
    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/donate_blood', methods=['GET', 'POST'])
@login_required
def donate_blood():
    if request.method == 'POST':
        donor_name = request.form['donar_name']
        age = request.form['age']
        date = request.form['date']
        phone = request.form['phone']
        city = request.form['city']
        disease = request.form['disease']
        blood_type = request.form['blood_type']
        user_id = session['user_id']

        conn = get_donor_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO blood_donations (donar_name, age, phone, city, disease, blood_type, date, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (donor_name, age, phone, city, disease, blood_type, date, user_id))

            conn.commit()
            flash('Blood donation submitted successfully!', 'success')
            return redirect(url_for('user_donation_history'))
        except sqlite3.Error as e:
            flash(f'An error occurred: {e}', 'error')
        finally:
            conn.close()

    return render_template('donate_blood.html')

@app.route('/request_blood', methods=['GET', 'POST'])
@login_required
def request_blood():
    if request.method == 'POST':
        patient_name = request.form['full_name']
        age = int(request.form['age'])
        phone = request.form['phone']
        hospital = request.form['hospital']
        city = request.form['city']
        blood_type = request.form['blood_type']
        units = request.form['units']
        user_id = session['user_id']  # Get the logged-in user's ID

        conn = get_request_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO blood_requests (patient_name, age, phone, hospital, city, blood_type, units, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (patient_name, age, phone, hospital, city, blood_type, units, user_id))

            conn.commit()
            flash('Blood request submitted successfully!', 'success')
            return redirect(url_for('user_request_history'))
        except sqlite3.Error as e:
            flash(f'An error occurred: {e}', 'error')
        finally:
            conn.close()

    return render_template('request_blood.html')


@app.route('/request_history')
@admin_login_required
def request_history():
    conn = get_request_db_connection()  # Connect to the request_data.db
    cursor = conn.cursor()

    # Fetch all blood requests from the database
    cursor.execute('SELECT * FROM blood_requests ORDER BY request_date DESC')
    requests = cursor.fetchall()
    conn.close()

    # Render the request_history template and pass the request data
    return render_template('request_history.html', requests=requests)


@app.route('/donation_history')
@admin_login_required
def donation_history():
    conn = get_donor_db_connection()  # Add parentheses to call the function
    cursor = conn.cursor()

    # Ensure you're querying the correct table (likely 'blood_donations')
    cursor.execute('SELECT * FROM blood_donations ORDER BY donation_date DESC')
    donations = cursor.fetchall()
    conn.close()

    # Render the donation_history template and pass the donations data
    return render_template('donation_history.html', donations=donations)

@app.route('/user_donation_history')
@login_required  # Ensure only logged-in users can access this page
def user_donation_history():
    user_id = session.get('user_id')  # Assuming user ID is stored in the session when logged in
    conn = get_donor_db_connection()  # Assuming this returns a valid DB connection
    cursor = conn.cursor()

    # Query to fetch donation history for the specific user
    cursor.execute('SELECT * FROM blood_donations WHERE user_id = ? ORDER BY donation_date DESC', (user_id,))
    user_donations = cursor.fetchall()  # Fetch the specific user's donation records
    conn.close()

    # Pass the donation data to the template
    return render_template('user_donation_history.html', user_donations=user_donations)


@app.route('/user_request_history')
@login_required
def user_request_history():
    user_id = session['user_id']  # Get the logged-in user's ID
    conn = get_request_db_connection()
    cursor = conn.cursor()

    # Fetch blood requests made by the logged-in user
    cursor.execute('''
        SELECT * FROM blood_requests 
        WHERE user_id = ?
        ORDER BY request_date DESC
    ''', (user_id,))
    requests = cursor.fetchall()
    conn.close()

    return render_template('user_request_history.html', requests=requests)



# Route for admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_logged_in' in session:
        return render_template('admin_dashboard.html')
    else:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))


# Route for forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        identifier = request.form['identifier']  # Username or email

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the identifier is an email
        cursor.execute('SELECT * FROM users WHERE email = ? OR username = ?', (identifier, identifier))
        user = cursor.fetchone()

        conn.close()

        if user:
            # Redirect the user to a password reset form where they can reset their password
            flash('User found. Please reset your password.', 'success')
            return redirect(url_for('reset_password', user_id=user['id']))
        else:
            flash('The username or email is not registered.', 'error')

    return render_template('forgot_password.html')


# Route for reset password
@app.route('/reset_password/<user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            hashed_password = generate_password_hash(new_password)  # Hash the password for security

            # Update the password in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
            conn.commit()
            conn.close()

            flash('Your password has been reset successfully. You can now log in.', 'success')
            return redirect(url_for('user_login'))
        else:
            flash('Passwords do not match. Please try again.', 'error')

    return render_template('reset_password.html', user_id=user_id)


# Route for contact us page
@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(debug=True)
