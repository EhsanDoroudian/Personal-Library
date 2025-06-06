$(document).ready(function() {
    // Form submission handling
    $('#logoutForm').on('submit', function(e) {
        const submitButton = $('#submitLogout');
        const buttonText = $('.button-text');
        const spinner = $('.spinner-border');

        submitButton.prop('disabled', true);
        buttonText.addClass('d-none');
        spinner.removeClass('d-none');
        // Form submits naturally to the server
    });
});