from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Define the path for the CSV file
CSV_FILE_PATH = 'data/users_data.csv'

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for admin login page
@app.route('/admin_login')
def admin_login():
    return render_template('admin-login.html')

# Route for user login page
@app.route('/user_login')
def user_login():
    return render_template('login-page.html')

# Route for create account page
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Extract form data
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        blood_type = request.form['blood_type']
        username = request.form['username']
        password = request.form['password']

        # Append form data to CSV file
        with open(CSV_FILE_PATH, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([full_name, email, phone, city, blood_type, username, password])

        return redirect(url_for('home'))

    return render_template('create_account.html')

# Route for contact us page
@app.route('/connect_us')
def connect_us():
    return render_template('contact-us.html')

if __name__ == '__main__':
    # Ensure the 'data' directory exists
    os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)
    
    app.run(debug=True)
