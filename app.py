from flask import Flask, render_template, request, redirect, url_for
from accordion import accordion_function
import sqlite3
from faker import Faker

app = Flask(__name__)
fake = Faker()


@app.route('/')
def home():
    room_data = accordion_function()
    room_numbers = [4118, 4119, 4120, 4121, 4122]
    room_info = [{'room': room_number, 'status': status} for room_number, status in zip(room_numbers, room_data)]
    return render_template("home.html", room_info=room_info)

@app.route('/booking')
def booking():
    return render_template("BookRoom.html")

@app.route('/information')
def information():
    return render_template("Information.html")
@app.route('/fake_booking')
def fake_booking():
    return fake_group_room()

@app.route('/submit_booking', methods=['POST']) #this function will be called when the user clicks the submit button on the form
def submit_booking():
    if request.method == 'POST': #if the user has submitted the form
        room_number = request.form.get('room') #get the room number from the form

        fake_datetime = fake.date_time_this_year() #generate a fake date and time for the booking in the current year.

        conn = sqlite3.connect('booking.db') #connect to the database
        cursor = conn.cursor() #cursor is a pointer to the database. It is used to execute SQL commands

        try:

def fake_group_room():
    fake_bookings = [fake.date_time_this_year() for _ in range(5)] #Generate 5 fake booking dates
    
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor() #cursor is a pointer to the database. It is used to execute SQL commands
    
    try: #try to insert the fake bookings data into the database
        for room_number in [4118, 4119, 4120, 4121, 4122]:
            for timeslot in fake_bookings: #for each fake booking date
                cursor.execute("INSERT INTO bookings (timeslot) VALUES (?)", (timeslot,)) 
            conn.commit() #commit the changes to the database 
            return  'Fake bookings succesfully added'
    except Exception as e: #if there is an error
        print("Error adding fake bookings")
        conn.rollback() #undo the changes
        return 'Error adding the fake bookings'
    finally: #close the connection to the database
        conn.close() 

    if __name__ == '__main__':
        app.run(debug=True) #debug=True means that the server will reload itself each time you make a change to the code
