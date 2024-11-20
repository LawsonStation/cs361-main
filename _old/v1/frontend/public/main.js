// DOMContentLoaded event listener to run only after the DOM is fully loaded.
document.addEventListener('DOMContentLoaded', function() {
    
    // JavaScript function to navigate to a new URL
    document.getElementById('navigateButton').addEventListener('click', function() {
        window.location.href = 'https://www.google.com';
    });

    // JavaScript function to navigate to a new URL
    document.getElementById('createListingButton').addEventListener('click', function() {
        window.location.href = 'create_listing.html';
    });
});
