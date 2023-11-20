from flask import Flask, render_template, request
from accordion import accordion_function
import sqlite3
from faker import Faker

app = Flask(__name__)
fake = Faker()

# Set up logging
logging.basicConfig(level=logging.ERROR)  # Adjust the logging level as needed. This will help us in debugging issues and understanding the cause of any errors that occur during the fake booking generation process.
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

def fake_group_room():
    fake_bookings = [fake.date_time() for _ in range(5)] #Generate 5 fake booking dates
    
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor() #cursor is a pointer to the database. It is used to execute SQL commands
    
    try: #try to insert the fake bookings data into the database
        for timeslot in fake_bookings: #for each fake booking date
            cursor.execute("INSERT INTO bookings (timeslot) VALUES (?)", (timeslot,)) 
        conn.commit() #commit the changes to the database 
        return  'Fake bookings succesfully added'
    except Exception as e: #if there is an error
        print("Error adding fake bookings")
        conn.rollback() #undo the changes
        return 'Error adding the fake bookings'
    finally: #close the connection to the database
        conn.close() #  

    if __name__ == '__main__':
    app.run(debug=True) #debug=True means that the server will reload itself each time you make a change to the code
