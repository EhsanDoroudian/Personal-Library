$(document).ready(function() {
    // Add active class to current nav link
    $('.nav-link').each(function() {
        if (this.href === window.location.href) {
            $(this).addClass('active');
        }
    });

    // Smooth scroll for footer links
    $('.footer a').on('click', function(e) {
        if (this.hash !== '') {
            e.preventDefault();
            const hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800);
        }
    });
});