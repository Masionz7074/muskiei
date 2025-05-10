// public/script.js

// Function to handle form submission
async function handleSubmit(event, endpoint) {
    event.preventDefault(); // Prevent the default form submission

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries()); // Convert form data to a plain object

    const messageElement = document.getElementById(endpoint === '/api/signup' ? 'signupMessage' : 'loginMessage');
    messageElement.textContent = 'Processing...';
    messageElement.className = 'message'; // Reset classes

    try {
        // Send data to the backend API using relative paths
        // Vercel will automatically route /api/signup to api/signup.py
        // and /api/login to api/login.py
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json(); // Assuming the backend sends JSON responses

        if (response.ok) { // Check if the HTTP status is 2xx (200, 201, etc.)
            messageElement.textContent = result.message || 'Success!';
            messageElement.className = 'message success';

            // --- Actions on Success ---
            if (endpoint === '/api/login') {
                 alert("Login Successful!"); // Replace with actual redirect or UI update
                 // Example: Redirect to a protected page
                 // window.location.href = '/dashboard.html';

                 // In a real app, the backend would send a session cookie or token
                 // and you'd handle storing and using it here for subsequent requests.

            } else if (endpoint === '/api/signup') {
                 // Example: Clear the form and suggest logging in
                 form.reset();
                 alert("Signup Successful! You can now login."); // Replace with actual action
                 // Optional: redirect to login page after a delay
                 // setTimeout(() => { window.location.href = '/index.html'; }, 2000);
            }

        } else {
            // Handle errors (e.g., validation errors, user exists, incorrect credentials)
            messageElement.textContent = result.error || 'An error occurred.';
            messageElement.className = 'message error';
             // Log specific error from backend if available
            console.error("Backend Error:", result.error);
        }

    } catch (error) {
        console.error('Fetch error:', error);
        messageElement.textContent = 'Network error. Could not connect to server or process response.';
        messageElement.className = 'message error';
    }
}

// Add event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');

    if (signupForm) {
        signupForm.addEventListener('submit', (event) => handleSubmit(event, '/api/signup'));
    }

    if (loginForm) {
        loginForm.addEventListener('submit', (event) => handleSubmit(event, '/api/login'));

         // Optional: Add keypress listener to login form for Enter key
         const loginUsernameInput = document.getElementById('loginUsername');
         const loginPasswordInput = document.getElementById('loginPassword');

         if (loginUsernameInput) {
             loginUsernameInput.addEventListener('keypress', function(event) {
                 if (event.key === 'Enter') {
                     event.preventDefault();
                     // Dispatch submit event on the form
                     event.target.form.dispatchEvent(new Event('submit'));
                 }
             });
         }
         if (loginPasswordInput) {
              loginPasswordInput.addEventListener('keypress', function(event) {
                 if (event.key === 'Enter') {
                     event.preventDefault();
                     // Dispatch submit event on the form
                     event.target.form.dispatchEvent(new Event('submit'));
                 }
             });
         }
    }
});