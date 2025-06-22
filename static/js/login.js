
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.querySelector('.toggle-password');
    const passwordInput = document.querySelector('input[type="password"], input[name="password"]');

    let timeoutId = null;

    if (toggleBtn && passwordInput) {
        toggleBtn.addEventListener('click', function () {
            const icon = toggleBtn.querySelector('i');
            const isCurrentlyPassword = passwordInput.getAttribute('type') === 'password';

            // Switch type
            passwordInput.setAttribute('type', isCurrentlyPassword ? 'text' : 'password');
            icon.classList.toggle('fa-eye', !isCurrentlyPassword);
            icon.classList.toggle('fa-eye-slash', isCurrentlyPassword);

            // If changing to text, set a timeout to change it back
            if (isCurrentlyPassword) {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    passwordInput.setAttribute('type', 'password');
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }, 5000);
            } else {
                // If user manually hides it again, cancel the timer
                clearTimeout(timeoutId);
            }
        });
    }
});

