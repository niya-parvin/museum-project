// Get references to the password input and the show button
const passwordInput = document.getElementById('password');
const showButton = document.querySelector('.show-button');

// Add an event listener to the show button
showButton.addEventListener('click', function() {
    // Check the current type of the password input
    if (passwordInput.type === 'password') {
        // Change the type to text to show the password
        passwordInput.type = 'text';
        // Change the button text or style if needed
        showButton.textContent = 'HIDE'; // Change button text to HIDE
    } else {
        // Change the type back to password to hide the password
        passwordInput.type = 'password';
        // Change the button text or style back
        showButton.textContent = 'SHOW'; // Change button text to SHOW
    }
});