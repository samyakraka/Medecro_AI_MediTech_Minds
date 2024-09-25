document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              localStorage.setItem('userSession', JSON.stringify(data.user)); // Store session in localStorage
              window.location.href = 'main.html'; // Redirect to main page
          } else {
              alert('Invalid credentials');
          }
      });
});
