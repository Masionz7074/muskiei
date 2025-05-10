# api/login.py
import os
import json
from vercel_kv import storage # Use vercel-kv library for KV interaction
import bcrypt # For password hashing

# Initialize Vercel KV client using environment variables set in Vercel
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
def handler(request):
    # Set CORS headers - same as signup.py
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
            # Read the request body (JSON)
            body = json.loads(request.body.decode('utf-8'))

            username = body.get('username')
            password = body.get('password')

            # --- Input Validation ---
            if not username or not password:
                return (json.dumps({"error": "Missing username or password"}), 400, headers)

            # --- Retrieve user from KV ---
            # Use lowercase username to match the key used during signup
            user_data_json = kv.get(f"user:{username.lower()}")

            if user_data_json is None or user_data_json == '':
                # User not found (or key didn't exist/returned empty string)
                return (json.dumps({"error": "Invalid username or password"}), 401, headers) # 401 Unauthorized

            # Parse the stored JSON string back to a Python object
            user_data = json.loads(user_data_json)
            stored_password_hash = user_data.get('password_hash')

            if not stored_password_hash:
                 # Should not happen if signup worked, but good defensive check
                 print(f"User {username.lower()} found but no password_hash stored.")
                 return (json.dumps({"error": "Could not verify password"}), 500, headers)


            # --- Verify Password ---
            # bcrypt.checkpw takes bytes for both the entered password and the stored hash
            entered_password_bytes = password.encode('utf-8')
            stored_password_hash_bytes = stored_password_hash.encode('utf-8')

            if bcrypt.checkpw(entered_password_bytes, stored_password_hash_bytes):
                # --- Login Successful ---
                # In a real application, you would create a session or issue a token here
                # and return it to the frontend so the user stays logged in for future requests.
                # For this example, we just return a success message and the username.
                print(f"User logged in: {username}") # This appears in Vercel function logs
                return (json.dumps({"message": "Login successful!", "username": user_data.get('username')}), 200, headers) # 200 OK

            else:
                # Password does not match the stored hash
                return (json.dumps({"error": "Invalid username or password"}), 401, headers) # 401 Unauthorized

        except json.JSONDecodeError:
            # Handle case where the request body is not valid JSON
            return (json.dumps({"error": "Invalid JSON in request body"}), 400, headers)
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Login error: {e}") # Log the error on the server side
            return (json.dumps({"error": "Internal server error"}), 500, headers)

    else:
        # Method Not Allowed for other HTTP methods
        return (json.dumps({"error": "Method Not Allowed"}), 405, headers)

# Vercel expects a function named 'handler'
# The request object structure depends on the Vercel runtime and builder,
# but the pattern above (request.method, request.body, request.headers) is common.