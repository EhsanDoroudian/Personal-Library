$(document).ready(function() {
    // Form submission handling
    $('#loginForm').on('submit', function(e) {
        const form = this;
        const submitButton = $('#submitLogin');
        const buttonText = $('.button-text');
        const spinner = $('.spinner-border');

        if (form.checkValidity() === false) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            submitButton.prop('disabled', true);
            buttonText.addClass('d-none');
            spinner.removeClass('d-none');
            // Form submits naturally to the server
        }
        form.classList.add('was-validated');
    });

    // Clear invalid feedback on input
    $('#id_login, #id_password').on('input', function() {
        $(this).removeClass('is-invalid');
        $(this).siblings('.invalid-feedback').remove();
    });
});