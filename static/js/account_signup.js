$(document).ready(function() {
    // Form validation and submission handling
    $('#signupForm').on('submit', function(e) {
        const form = this;
        const submitButton = $('#submitSignup');
        const buttonText = $('.button-text');
        const spinner = $('.spinner-border');
        const password1 = $('#id_password1').val();
        const password2 = $('#id_password2').val();

        // Validate passwords match
        if (password1 && password2 && password1 !== password2) {
            e.preventDefault();
            $('#id_password2').cssClass('is-invalid');
            $('#id_password2').siblings('.invalid-feedback').remove();
            $('#id_password2').after('<div class="invalid-feedback d-block">رمزهای عبور مطابقت ندارند.</div>');
            return;
        }

        if (form.checkValidity() === false) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            submitButton.prop('disabled', true);
            buttonText.addClass('d-none');
            spinner.removeClass('d-none');
            // Form submits naturally to the server
        }
        form.addClass('was-validated');
    });

    // Clear invalid feedback on input
    $('#id_password1, #id_password2').on('input', function() {
        $(this).removeClass('is-invalid');
        $(this).siblings('.invalid-feedback').remove();
    });
});