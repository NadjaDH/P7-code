var checkedValues = [] // Array to store the checked values
let selectedRoomNumber; // Variable to store the selected room number
let selectedDate; // Variable to store the selected date
var bookedTimeslots = []; // Array to store the booked timeslots
var bookButton = document.getElementById('bookButton'); // Get the book button

// Made variables since we did the same in html where we hardcoded dates, used in weeklyCalendar()
var dates = new Map();
dates.set('Mon', '2023-11-20')
dates.set('Tue', '2023-11-21')
dates.set('Wed', '2023-11-22')
dates.set('Thu', '2023-11-23')
dates.set('Fri', '2023-11-24')

/*function isTimeslotBooked(timeslot) { //The function isTimeslotBooked(timeslot) checks if a given timeslot is already booked.
    alert(bookedTimeslots);
    return bookedTimeslots.includes(timeslot);
}*/

async function isTimeslotBooked(timeslot, room, selected_date) {
    var booked = false;
    const response = await fetch('/is_timeslot_booked', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            timeslot: timeslot, // Include the array of checked values
            room: room, // Include the room number
            date: selected_date, // Include the date
        })
    })
        .then(response => response.json()) // Parse the response as JSON
        .then(data => { // Log the data to the console
            if (data.error) {
                alert(data.error);
            } else {
                //If there's no error message, the booking was successful
                console.log('Success:', data);
                if(data.message) booked = true;
            }
        })
        .catch((error) => {  // Catch any errors 
            console.error('Error:', error); // Log the error to the console
        });
        return booked;
}

function displayCheckbox() {
    // get all checkboxes on the page
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    
    // check if any checkbox is checked and store the number of checked checkboxes
    var checkedCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;
    
    // get the button element
    var button = document.getElementById('bookButton');
    
    // enable or disable the button based on how many checkboxes are checked
    button.disabled = checkedCount === 0 || checkedCount > 4 || !selectedRoomNumber;
    
    // set the value of the hidden input field for each checkbox ***WHAT DOES THIS DO IT GAVE ME ERRORS 
    /*checkboxes.forEach((checkbox, index) => {
        var timeslotInput = document.getElementById('timeslot-' + (index + 1));
        if (checkbox.checked) {
            timeslotInput.value = checkbox.getAttribute('data-timeslot');
        } else {
            timeslotInput.value = '';
        }
    });*/
}

async function weeklyCalendar(){
    var slots = ['07:00 - 08:00', '08:00 - 09:00', '09:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00',
                '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00', '15:00 - 16:00']; // needed to make timeslots because I wasn't sure how to make it work with starttime endtime
    var daysContainers = document.querySelectorAll('div[class="days-container"]'); // Select all elements with class "days-container", which is only our weeklycalendar

    Array.from(daysContainers).forEach( async (container) => {     // Iterate over each "days-container" and extract the room number from the container's ID and the child nodes (days of the week) of the container
        var roomNumber = "Room " + container.id.substring(container.id.lastIndexOf(" ") + 1);
        var daysOfWeek = container.childNodes;
       // console.log(roomNumber);
        daysOfWeek.forEach(async (day) => {
            day.style.backgroundColor = '#B3D93A'; // Green for 3 or less bookings
            var checkedCount = 0; // Counter for checked bookings
            slots.forEach( async (slot) => { // Iterate over each time slot
                var booked = await isTimeslotBooked(slot, roomNumber, dates.get(day.textContent)); // Check if the current time slot is booked for the specific room and date

                if (booked){
                    checkedCount++;
                    if (checkedCount <= 3) {
                        day.style.backgroundColor = '#B3D93A'; // Green for 3 or less bookings
                    } else if (checkedCount <= 8) {
                        day.style.backgroundColor = '#FFD700'; // Yellow for partially booked (4-8 bookings)
                    } else {
                        day.style.backgroundColor = '#F16B5C'; // Red for fully booked
                    }
                }
            });
        });
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

function OpenDay(evt, day, selectedDate) { // Tabbar functionality
    var i, tabcontent, tablinks; 
    
    var dayOfWeek = (parseInt(day) - 1) % 7; //Convert the day of the week to a number between 0 and 6
    
    //Initialize variable with the function to check if the day of the week is before
    var buttonDisabled = hasDayPassed(dayOfWeek);
        
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

    resetCheckboxes(); // Reset the checkboxes when a new tab is opened
}

function selectDate(date) {
    // Sets the global variable selectedDate to the value of date passed into the function.
    selectedDate = date;
    //Retrieves the hidden input field with the id selectedDateInput.
    var selectedDateInput = document.getElementById('selectedDateInput');
    //Sets the value of the hidden input field to the date passed into the function.
    selectedDateInput.value = date;
}

function resetCheckboxes() { // Reset the checkboxes when a new tab is opened
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(async (checkbox) => {
        console.log(checkbox.value);
        var booked = await isTimeslotBooked(checkbox.value, selectedRoomNumber, selectedDate);
        if (booked){
            checkbox.disabled = true;
        }
        else checkbox.disabled = false;
        checkbox.checked = false;
    });
}

function hasDayPassed(daysOfWeek) { //Function to check if the day of the week is before the current day
    var now = new Date();
    var currentDay = now.getDay();

    if (currentDay === 0 || currentDay === 6) {
        return false; //If it's Saturday or Sunday, return false
    }

    return currentDay > daysOfWeek; //Return true if the current day is after the day of the week
}

// javascript for closing the dropdown menu when a room is selected
function SelectRoom(room) {
    console.log("SelectRoom function called with room: ", room); // Debugging line
    selectedRoomNumber = room // Set the selected room number to the room that was clicked
    
    //var bookButton = document.getElementById("bookButton");
    if (bookButton) {
        // Disable the book button if no room or no checkboxis selected 
        bookButton.disabled = !selectedRoomNumber || !checkboxChecked(); 
    }
    
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
    // Once a room is selected, automatically open tab for current day - CoPilot
    var dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
    var date = new Date();
    // Get abbreviation for current day - note: getDay() returns 0 for Sunday, 1 for Monday, etc., so we subtract 1 to align with our array
    var dayOfWeek = dayNames[date.getDay() - 1];
    if (date.getDay() === 0 || date.getDay() === 6) {
        dayOfWeek = 'Mon'; // defaults to Monday if it's Saturday or Sunday
    }
    // Find the element with the ID of the current day (or 'Mon' if it's Saturday or Sunday) and simulate a click on it
    document.getElementById(dayOfWeek).click();
    resetCheckboxes(); // Reset the checkboxes when a new room is selected
}

//Function to check if any checkboxes are checked
function checkboxChecked() { 
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    return Array.from(checkboxes).some(checkbox => checkbox.checked); //ChatGPT
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
        .then(data => { 
            if (data.message) {
                alert(data.message);
            } else {
                alert(data.error);
            }
        })
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
        })
    })
        .then(response => response.json()) // Parse the response as JSON
        .then(data => { // Log the data to the console
            if (data.error) {
                alert(data.error);
            } else {
                //If there's no error message, the booking was successful
                console.log('Success:', data);
                alert("Room booked! Booking ID: " + data.booking_id);
            }
        })
        .catch((error) => {  // Catch any errors and log them to the console
            console.error('Error:', error); // Log the error to the console
        });
        resetCheckboxes();
}

// JavaScript function to change background color
function checkIn() {
    if (selectedRoomNumber) {
        // Remove the "Room " part from selectedRoomNumber before appending it to the URL
        fetch('/check_in_room/' + selectedRoomNumber, {method: 'POST'});
        alert("You are now checked in!")
    } else {
        alert("Please select a room first.");
    }
} 

function checkOut() {
    if (selectedRoomNumber) {
        // Remove the "Room " part from selectedRoomNumber before appending it to the URL
        fetch('/check_out_room/' + selectedRoomNumber, {method: 'POST'});
        alert("You are now checked out!")
    } else {
        alert("Please select a room first.");
    }
}

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
weeklyCalendar();
updateClock();
setInterval(updateClock, 1000);
setInterval(updateClock, 1000);
window.onload = displayCheckbox; // Call the displayCheckbox function when the page is loaded
