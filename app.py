from flask import Flask, request, jsonify
# You'll need a library for secure password hashing, e.g., bcrypt
# from flask_bcrypt import Bcrypt # pip install Flask-Bcrypt
# You'll need a library for database interaction, e.g., sqlite3 (built-in), psycopg2 (PostgreSQL), mysql.connector (MySQL), pymongo (MongoDB), etc.
# import sqlite3 # For example using SQLite

app = Flask(__name__)
# bcrypt = Bcrypt(app) # Initialize Bcrypt

# --- !!! INSECURE PLACEHOLDER "DATABASE" !!! ---
# In a real app, this would be a proper database connection and operations
# This list stores passwords in PLAIN TEXT - DO NOT DO THIS IN PRODUCTION!
# This list is also reset every time the server restarts - NOT persistent
users_db = [] # Example structure: [{'username': '...', 'password_hash': '...', 'phone': '...'}]
# --- !!! END INSECURE PLACEHOLDER !!! ---


# --- Helper for placeholder DB (find user) ---
def find_user(username):
    for user in users_db:
        if user['username'] == username:
            return user
    return None

# --- Helper for placeholder DB (add user) ---
def add_user(username, password_hash, phone):
     if find_user(username):
         return False # User already exists
     users_db.append({'username': username, 'password_hash': password_hash, 'phone': phone})
     print(f"User signed up: {username}")
     print("Current placeholder DB:", users_db) # For demonstration
     return True


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')

    # --- BASIC INPUT VALIDATION (ADD MORE!) ---
    if not username or not password or not phone:
        return jsonify({"error": "Missing username, password, or phone number"}), 400

    # --- !!! SECURITY FLAW !!! ---
    # In a real app, you would HASH the password here:
    # password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # Storing the plain password below is DANGEROUS!
    insecure_plain_password = password
    # --- !!! END SECURITY FLAW !!! ---

    # --- INSECURE PLACEHOLDER DB OPERATION ---
    # In a real app, you'd insert username, password_hash, and phone into your SQL/NoSQL database
    success = add_user(username, insecure_plain_password, phone) # Using plain password placeholder

    if success:
        return jsonify({"message": "User signed up successfully!"}), 201 # 201 Created
    else:
        return jsonify({"error": "Username already exists"}), 409 # 409 Conflict


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # --- BASIC INPUT VALIDATION ---
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # --- INSECURE PLACEHOLDER DB OPERATION ---
    # In a real app, you'd retrieve the user from the database by username
    user = find_user(username) # Using placeholder find

    if user:
        # --- !!! SECURITY FLAW !!! ---
        # In a real app, you would COMPARE the HASH of the entered password
        # with the stored password_hash:
        # if bcrypt.check_password_hash(user['password_hash'], password):
        # Comparing plain passwords below is DANGEROUS!
        if user['password_hash'] == password: # Comparing plain password placeholder
            # --- REAL LOGIN SUCCESS ---
            # In a real app, you'd create a session or issue a token here
            print(f"User logged in: {username}") # For demonstration
            return jsonify({"message": "Login successful!"}), 200
        else:
            # Password doesn't match hash
            return jsonify({"error": "Invalid username or password"}), 401 # 401 Unauthorized
    else:
        # User not found
        return jsonify({"error": "Invalid username or password"}), 401 # 401 Unauthorized

@app.route('/')
def index():
    # Flask serves the index.html file located in a 'templates' folder by default
    # For this simple example, we'll just show a basic message.
    # You would configure Flask to serve your static index.html and signup.html,
    # or use a web server like Nginx/Apache to serve static files and proxy API requests to Flask.
    return "Backend is running. Access /signup.html or /index.html (served separately or configured via Flask) to use the forms."


if __name__ == '__main__':
    # When running locally, the Flask server will run on http://127.0.0.1:5000/
    # You'll need to configure your frontend script.js to send requests to this address
    # if running them separately during development.
    # For production, you'd need proper deployment and URL configuration.
    app.run(debug=True) # debug=True is helpful for development, turn off for production