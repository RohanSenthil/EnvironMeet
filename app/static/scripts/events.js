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
     // Function to convert a date string to a Date object
  function parseDate(dateStr) {
    const [year, month, day] = dateStr.split('-');
    return new Date(year, month - 1, day);
  }

  // Function to compare two event cards based on their dates
  function compareEventDates(eventCard1, eventCard2) {
    const dateStr1 = eventCard1.querySelector('.card-meta--date').textContent.trim();
    const dateStr2 = eventCard2.querySelector('.card-meta--date').textContent.trim();

    const date1 = parseDate(dateStr1);
    const date2 = parseDate(dateStr2);

    return date1 - date2;
  }

  // Get the container that holds all event cards
  const eventsContainer = document.querySelector('.EventsContainer1');

  // Get all event cards within the container
  const eventCards = Array.from(eventsContainer.querySelectorAll('.eventCard'));

  // Sort the event cards based on their dates
  eventCards.sort(compareEventDates);

  // Clear the container
  eventsContainer.innerHTML = '';

  // Append the sorted event cards back to the container
  eventCards.forEach((eventCard) => {
    eventsContainer.appendChild(eventCard);
  });

//const searchBar = document.getElementbyId('searchBar');
//const eventCards = document.querySelectorAll('.eventCard');
//
//searchBar.addEventListener('keyup', event => {
//    const searchTerm = searchBar.value.toLowerCase();
//
//    eventCards.forEach(card => {
//        const eventName = card.querySelector('.card-header h3').textContent.toLowerCase();
//
//        if (eventName.includes(searchTerm)) {
//            card.style.display = 'block';
//        } else {
//            card.style.display = 'none';
//        }
//    });
//});

function search() {
  // Declare variables
  var input, filter;
  input = document.getElementById("dainput");
  filter = input.value.toUpperCase();
  cards = document.getElementsByClassName("eventCard")
  names = document.getElementsByClassName("card-header");

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < cards.length; i++) {
    a = names[i];
    if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
      cards[i].style.display = "";
    } else {
      cards[i].style.display = "none";
    }
  }
}