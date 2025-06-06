$(document).ready(function() {
    // Client-side search functionality
    $('#searchInput').on('input', function() {
        const query = $(this).val().toLowerCase();
        $('.book-item').each(function() {
            const title = $(this).data('title').toLowerCase();
            const author = $(this).data('author').toLowerCase();
            const user = $(this).data('user').toLowerCase();
            if (title.includes(query) || author.includes(query) || user.includes(query)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Clear search input
    $('#searchButton').on('click', function() {
        $('#searchInput').val('').trigger('input');
    });
});