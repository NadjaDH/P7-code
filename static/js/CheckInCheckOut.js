// On the page with the indicator, use this code to set the background color when the page loads
window.onload = function() {
    var color = localStorage.getItem('backgroundColor'); // Get the color from local storage
    if (color) {
        changeBackgroundColor(color); // Change the background color
    }
};