// From original main.js - form validation, SSE for notifications
document.addEventListener('DOMContentLoaded', function() {
    // Login validation from original
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.querySelector('#username').value;
            const password = document.querySelector('#password').value;
            if (!username || !password) {
                e.preventDefault();
                alert('Username and password required.');
            }
        });
    }

    // SSE for real-time announcements/notifications from original
    if (typeof(EventSource) !== 'undefined') {
        const source = new EventSource('/stream_messages');
        source.onmessage = function(event) {
            const data = JSON.parse(event.data);
            // Add notification toast or update UI
            console.log('New message:', data);
        };
    }

    // Theme toggle from original
    const themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            // Save to preferences via AJAX
        });
    }
});