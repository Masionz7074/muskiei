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
        // Send data to the backend API
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json(); // Assuming the backend sends JSON responses

        if (response.ok) { // Check if the HTTP status is 2xx
            messageElement.textContent = result.message || 'Success!';
            messageElement.className = 'message success';
            // Redirect or update UI on successful login/signup
            if (endpoint === '/api/login') {
                 // Example: Redirect to a dashboard or show logged-in content
                 alert("Login Successful! (Placeholder)"); // Replace with actual redirect
                 // window.location.href = '/dashboard.html'; // Example redirection
            } else if (endpoint === '/api/signup') {
                 // Example: Clear the form or redirect to login
                 form.reset();
                 alert("Signup Successful! You can now login. (Placeholder)"); // Replace with actual action
                 // window.location.href = '/index.html'; // Example redirection
            }

        } else {
            // Handle errors (e.g., validation errors, user exists, incorrect credentials)
            messageElement.textContent = result.error || 'An error occurred.';
            messageElement.className = 'message error';
        }

    } catch (error) {
        console.error('Fetch error:', error);
        messageElement.textContent = 'Network error. Could not connect to server.';
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
    }
});