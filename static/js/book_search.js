$(document).ready(function() {
    // Form submission handling
    $('form').on('submit', function(e) {
        const input = $('input[name="q"]');
        if (!input.val().trim()) {
            e.preventDefault();
            input.addClass('is-invalid');
            input.siblings('.invalid-feedback').remove();
            input.after('<div class="invalid-feedback d-block">لطفاً عبارت جستجو را وارد کنید.</div>');
        }
    });

    // Clear invalid feedback on input
    $('input[name="q"]').on('input', function() {
        $(this).removeClass('is-invalid');
        $(this).siblings('.invalid-feedback').remove();
    });
});