document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const fname = document.getElementById('fname').value;
    const lname = document.getElementById('lname').value;
    const phone = document.getElementById('phone').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
    }

    const user = {
        firstName: fname,
        lastName: lname,
        phone: phone,
        email: email,
        password: password
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    }).then(response => {
        if (response.ok) {
            window.location.href = 'login.html'; // Redirect to login page
        } else {
            alert('Registration failed');
        }
    });
});
