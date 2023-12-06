var checkedValues = [] // Array to store the checked values
let selectedRoomNumber; // Variable to store the selected room number
let selectedDate; // Variable to store the selected date
var bookedTimeslots = []; // Array to store the booked timeslots

function isTimeslotBooked(timeslot) { //The function isTimeslotBooked(timeslot) checks if a given timeslot is already booked.
    return bookedTimeslots.includes(timeslot);
}



function displayCheckbox() {
    // Get all checkboxes on the page
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');

    // Check if any checkbox is checked and store the number of checked checkboxes
    var checkedCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;

    // Get the button element
    var button = document.getElementById('bookButton');

    // Enable or disable the button based on how many checkboxes are checked
    button.disabled = checkedCount === 0 || checkedCount > 4;

    // set the value of the hidden input field for each checkbox
    checkboxes.forEach((checkbox, index) => {
        var timeslotInput = document.getElementById('timeslot-' + (index + 1));
        if (checkbox.checked) {
            timeslotInput.value = checkbox.getAttribute('data-timeslot');
        } else {
            timeslotInput.value = '';
        }
    });
}

function displayAlert() { // This function is called when the big blue bookbutton is clicked

    // Get all checkboxes
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');

    // Det her er måske ikke nødvendigt
    // Get the values of the checked checkboxes
    var checkedValues = Array.from(checkboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);

    // Check if any checkbox is checked
    var checkedCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;
    // Get current total from localStorage and convert it to a number
    var totalChecked = Number(localStorage.getItem("checked")) || 0;
    // Add checkedCount to the total
    totalChecked += checkedCount;

    // Store the new total in localStorage
    localStorage.setItem("checked", totalChecked);
    // Log the new total to the console
    console.log(localStorage.getItem("checked"))
    // Her stopper det unødvendige

    var roomNumber = document.getElementById('dropdownButton'); // Get the room number from the dropdown menu and store it in a variable called roomNumber
    // Send the checked values to the server
    submitBooking(checkedValues, selectedRoomNumber, selectedDate); // When the button is clicked, call the submitBooking function with the checked values, 
    //the room number and the selected date, that runs the code in the submitBooking

}

// javascript for tabbar
function OpenDay(evt, day, selectedDate) {
    var i, tabcontent, tablinks;

    var dayOfWeek = (parseInt(day) - 1) % 7; //Convert the day of the week to a number between 0 and 6

    //Initialize variable with the function to check if the day of the week is before
    var buttonDisabled = hasDayPassed(dayOfWeek);

    resetCheckboxes(); // Reset the checkboxes when a new tab is opened

    //If the button should be disabled, do nothing so that it is not possible to open the content
    if (buttonDisabled) {
        return;
    }

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    } //Hide all the content

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    } //Remove the active class from all the buttons

    document.getElementById(day).style.display = "block";
    evt.currentTarget.className += " active"; //Show the content of the button that was clicked

    // Call selectDate function with the selected date
    selectDate(selectedDate);
}

function selectDate(date) {
    // Sets the global variable selectedDate to the value of date passed into the function.
    selectedDate = date;
    //Retrieves the hidden input field with the id selectedDateInput.
    var selectedDateInput = document.getElementById('selectedDateInput');
    //Sets the value of the hidden input field to the date passed into the function.
    selectedDateInput.value = date;
}
// Reset the checkboxes when a new tab is opened
function resetCheckboxes() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach((checkbox) => {
        checkbox.checked = false;
    });
}

function hasDayPassed(daysOfWeek) { //Function to check if the day of the week is before the current day
    var now = new Date();
    var currentDay = now.getDay();
    return currentDay > daysOfWeek;
}

// javascript for closing the dropdown menu when a room is selected
function SelectRoom(room) {
    console.log("SelectRoom function called with room: ", room); // Debugging line
    selectedRoomNumber = room // Set the selected room number to the room that was clicked
    var dropdownButton = document.getElementById("dropdownButton");
    if (dropdownButton) { // Check if the element exists
        dropdownButton.innerText = room;
    } else {
        console.log("Element with id 'SelectRoom' not found"); // Debugging line
    }
    if (typeof toggleDropdown === "function") { // Check if toggleDropdown is defined
        toggleDropdown(); //Closes the dropdown menu after selecting a room
    } else {
        console.log("toggleDropdown is not defined"); // Debugging line
    }
}



// javascript for when the user clicks on the dropdown button, toggle between hiding and showing the dropdown content
function toggleDropdown() {
    document.getElementById("dropdownID").classList.toggle("show");
}

// javascript for closing the dropdown menu when clicking outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}



function cancelBooking(event) {
    // Prevent the form from submitting. Without event.preventDefault(), the form would be submitted twice: once by the default form submission behavior, and once by your JavaScript code. This could lead to unexpected results.
    event.preventDefault();
    // Get the booking ID from the form
    let bookingId = document.getElementById('cancelBookingID').value;

    // Create the formData object. This is the data that will be sent to the server
    let formData = {
        booking_id: bookingId
    };

    // Send the fetch request. This is an asynchronous function, so the code will continue to run while the request is being sent to the server
    fetch('cancel_booking_route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Set the content type to application/x-www-form-urlencoded
        },
        body: new URLSearchParams(formData).toString() // Convert the formData object to a URL encoded string
    })
        // TODO: Mangler alert.
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

function submitBooking(checkedValues, selectedRoomNumber, selectedDate, bookingID) {
    fetch('/submit_booking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            timeslots: checkedValues, // Include the array of checked values
            Room: selectedRoomNumber, // Include the room number
            date: selectedDate, // Include the date
            BookID: bookingID // Include the bookingID
        })
    })
        .then(response => response.json()) // Parse the response as JSON
        .then(data => { // Log the data to the console
            if (data.error) {
                alert(data.error);
            } else {
                //If there's no error message, the booking was successful
                console.log('Success:', data);
                alert("Room booked!");
            }
        })
        .catch((error) => {  // Catch any errors and log them to the console
            console.error('Error:', error); // Log the error to the console
        });
}
// JavaScript function to change background color
function changeBackgroundColor(color) {
    document.getElementById('myElement').style.backgroundColor = color;
}

// Add event listeners to the buttons
document.getElementById('checkInButton').addEventListener('click', function () {
    alert('You are now checked-in');
    localStorage.setItem('backgroundColor','green'); // Change to the color you want
});

document.getElementById('checkOutButton').addEventListener('click', function () {
    alert('You are now checked-out');
    localStorage.setItem('backgroundColor', 'red'); // Change to the color you want
});


// Update current day in javascript
function updateClock() {
    var now = new Date();
    var daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    var currentDay = now.getDay() + 1; //ChatGPT
    var buttons = document.getElementsByClassName("tablinks");

    //ChatGPT
    for (var i = 0; i < buttons.length; i++) { //Loop through all the buttons
        var buttonDay = i + 2; //Get the day of the week for the button
        buttons[i].disabled = buttonDay < currentDay; //Disable the button if the day of the week is before the current day
    }

    var dayname = daysOfWeek[now.getDay()];
    var month = months[now.getMonth()];
    var daynum = now.getDate();
    var year = now.getFullYear();

    document.getElementById('dayname').textContent = dayname;
    document.getElementById('month').textContent = month;
    document.getElementById('daynum').textContent = daynum;
    document.getElementById('year').textContent = year;
}

updateClock();
setInterval(updateClock, 1000);