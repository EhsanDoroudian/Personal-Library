$(document).ready(function() {
    // Form validation and submission handling
    $('#reviewForm').on('submit', function(e) {
        const form = this;
        const submitButton = $('#submitReview');
        const buttonText = $('.button-text');
        const spinner = $('.spinner-border');

        if (form.checkValidity() === false) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            e.preventDefault(); // Remove in production for actual submission
            submitButton.prop('disabled', true);
            buttonText.addClass('d-none');
            spinner.removeClass('d-none');
            setTimeout(() => {
                submitButton.prop('disabled', false);
                buttonText.removeClass('d-none');
                spinner.addClass('d-none');
                form.reset();
                form.classList.remove('was-validated');
            }, 2000); // Simulate submission
        }
        form.classList.add('was-validated');
    });
});