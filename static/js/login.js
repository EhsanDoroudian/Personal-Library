$(document).ready(function() {
    // Password toggle functionality
    $('.toggle-password').click(function() {
        const passwordField = $('#password');
        const type = passwordField.attr('type') === 'password' ? 'text' : 'password';
        passwordField.attr('type', type);
        $(this).toggleClass('fa-eye fa-eye-slash');
    });

    // Form validation and loading state
    $('#loginForm').on('submit', function(e) {
        const form = this;
        const submitButton = $('#submitButton');
        const buttonText = $('.button-text');
        const spinner = $('.spinner-border');

        if (form.checkValidity() === false) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            e.preventDefault(); // Remove this in production if you want form to submit
            submitButton.prop('disabled', true);
            buttonText.addClass('d-none');
            spinner.removeClass('d-none');
            setTimeout(() => {
                submitButton.prop('disabled', false);
                buttonText.removeClass('d-none');
                spinner.addClass('d-none');
            }, 2000); // Simulate loading
        }
        form.classList.add('was-validated');
    });
});