function toggleDropdown() {
  var dropdown = document.getElementById("myDropdown");
  dropdown.classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
};
    // Function to reset the inactivity timer
    function resetInactivityTimer() {
        fetch('/reset_activity', { method: 'POST' }); // Send a request to the server to reset the last_activity
    }

    // Add event listeners to reset the timer on user interaction
    document.addEventListener('click', resetInactivityTimer);
    document.addEventListener('keydown', resetInactivityTimer);

    // Call the resetInactivityTimer function on page load to start the timer
    resetInactivityTimer();