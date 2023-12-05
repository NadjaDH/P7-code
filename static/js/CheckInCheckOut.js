let selectedRoomNumber;

function checkIn() {
    var room = document.getElementById("SelectRoom".value);
    selectedRoomNumber = room
    document.getElementById("checkInModal").style.display = "block";
    document.getElementById("statusIndicator").style.backgroundColor = "#B3D93A"; // Checked-in color
}

function checkOut() {
    var room = document.getElementById("SelectRoom".value);
    selectedRoomNumber = room
    document.getElementById("checkOutModal").style.display = "block";
    document.getElementById("statusIndicator").style.backgroundColor = "#F16B5C"; // Checked-out color
}

