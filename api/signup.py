# api/signup.py
import os
import json
from vercel_kv import storage # Use vercel-kv library for KV interaction
import bcrypt # For password hashing

# Initialize Vercel KV client using environment variables set in Vercel
# Make sure KV_REST_API_URL and KV_REST_API_TOKEN are set in Vercel Project Settings
try:
    kv = storage.VercelKV(
        url=os.environ.get('KV_REST_API_URL'),
        token=os.environ.get('KV_REST_API_TOKEN'),
    )
    kv_initialized = True
except Exception as e:
    print(f"Error initializing Vercel KV client: {e}")
    kv_initialized = False


# Vercel Serverless Function entry point
# Vercel passes a request-like object as the first argument
def handler(request):
    # Set CORS headers to allow requests from your frontend domain on Vercel
    # Replace '*' with your specific Vercel domain in production for better security
    headers = {
        'Access-Control-Allow-Origin': '*', # Be more specific in production!
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json',
    }

    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        return (json.dumps({}), 200, headers)

    if request.method == 'POST':
        if not kv_initialized:
             return (json.dumps({"error": "Database not configured"}), 500, headers)

        try:
            # Vercel's request object typically has a .body attribute
            # Need to decode from bytes and parse JSON
            body = json.loads(request.body.decode('utf-8'))

            username = body.get('username')
            password = body.get('password')
            phone = body.get('phone')

            # --- Input Validation ---
            if not username or not password or not phone:
                return (json.dumps({"error": "Missing username, password, or phone number"}), 400, headers)

            # Basic validation (add more robust checks for production)
            if len(username) < 3:
                 return (json.dumps({"error": "Username must be at least 3 characters"}), 400, headers)
            if len(password) < 6:
                 return (json.dumps({"error": "Password must be at least 6 characters"}), 400, headers)
            # You might add phone number format validation here

            # --- Check if user already exists in KV ---
            # KV stores data as key-value pairs.
            # Use a consistent key format, like "user:<lowercase_username>"
            # vercel_kv's .get() returns None or potentially '' for non-existent keys
            user_data_json = kv.get(f"user:{username.lower()}")

            if user_data_json is not None and user_data_json != '':
                # User found, username already exists
                return (json.dumps({"error": "Username already exists"}), 409, headers) # 409 Conflict

            # --- Securely Hash the Password ---
            # bcrypt expects bytes, so encode the password string
            password_bytes = password.encode('utf-8')
            # Generate a salt and hash the password
            # bcrypt.gensalt() generates a random salt
            hashed_password_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            # Decode the hashed password bytes back to a string for storage
            hashed_password_string = hashed_password_bytes.decode('utf-8')

            # --- Store the new user in Vercel KV ---
            # We store a JSON string representing the user object
            user_data = {
                "username": username, # Store original case username if needed
                "password_hash": hashed_password_string,
                "phone": phone
                # DO NOT store the plain password
            }
            # Store using the lowercase username as the key for case-insensitive lookup
            kv.set(f"user:{username.lower()}", json.dumps(user_data))
            # Optional: set an expiration if users should be temporary
            # kv.set(f"user:{username.lower()}", json.dumps(user_data), ex=3600) # Expires in 1 hour

            # --- Success Response ---
            print(f"User signed up: {username}") # This appears in Vercel function logs
            return (json.dumps({"message": "User signed up successfully!"}), 201, headers) # 201 Created

        except json.JSONDecodeError:
            # Handle case where the request body is not valid JSON
            return (json.dumps({"error": "Invalid JSON in request body"}), 400, headers)
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Signup error: {e}") # Log the error on the server side
            return (json.dumps({"error": "Internal server error"}), 500, headers)

    else:
        # Method Not Allowed for other HTTP methods
        return (json.dumps({"error": "Method Not Allowed"}), 405, headers)

# Vercel expects a function named 'handler'
# The request object structure depends on the Vercel runtime and builder,
# but the pattern above (request.method, request.body, request.headers) is common.