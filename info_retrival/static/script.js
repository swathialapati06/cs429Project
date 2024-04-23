$(document).ready(function() {
    $('#search-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission behavior
        
        // Retrieve query and top K values from input fields
        var query = $('#query').val();
        var top = $('#top').val();
        
        // Check if both query and top K values are provided
        if (!query.trim() || !top.trim()) {
            alert('Please enter both query and top K value.');
            return;
        }
        
        // Make AJAX GET request to search route
        $.get('/search', { query: query, top: top }, function(data) {
            displayResults(data);
        });
    });

    // Function to display search results
    function displayResults(results) {
        $('#results').empty();
        results.forEach(function(result) {
            var articleHtml = '<div class="result">' +
                '<h2>' + result.headline + '</h2>' +
                '<p>' + result.article.substring(0, 500) + '...</p>' +
                '</div>';
            $('#results').append(articleHtml);
        });
    }
});
