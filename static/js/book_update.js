$(document).ready(function() {
    // Form validation and submission handling
    $('#bookForm').on('submit', function(e) {
        const form = this;
        const submitButton = $('#submitBook');
        const buttonText = $('.button-text');
        const spinner = $('.spinner-border');
        const shabakNum = $('#shabak_num').val().replace(/[-\s]/g, '');

        // Validate Shabak Number (10 or 13 digits)
        if (shabakNum && !/^\d{10,13}$/.test(shabakNum)) {
            e.preventDefault();
            $('#shabak_num').addClass('is-invalid');
            $('#shabak_num').next('.invalid-feedback').remove();
            $('#shabak_num').after('<div class="invalid-feedback d-block">شابک باید ۱۰ یا ۱۳ رقم باشد.</div>');
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
        form.classList.add('was-validated');
    });

    // Clear invalid feedback on input
    $('#shabak_num').on('input', function() {
        $(this).removeClass('is-invalid');
        $(this).next('.invalid-feedback').remove();
    });

    // Image preview
    $('#cover').on('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('.book-cover-preview').html(`<img src="${e.target.result}" alt="پیش‌نمایش جلد" class="img-fluid rounded shadow" style="max-height: 250px;">`);
            };
            reader.readAsDataURL(file);
        }
    });
});