$(document).ready(function () {
    // AJAX call for loading authors based on search term
    $("#author-select").select2({
        placeholder: 'Search User',
        ajax: {
            url: "/ajax/load-authors/",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    author_name: params.term, // Search term
                    page: params.page
                };
            },
            processResults: function (data) {
                return {
                    results: data.results
                };
            },
            cache: true
        }
    });
});