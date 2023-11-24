from flask import Flask, render_template, request, redirect, url_for, jsonify
from accordion import accordion_function
import sqlite3
from faker import Faker
from dateutil.parser import parse


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

def insert_booking(timeslots, room, date): #This function is used to insert a booking into the database. It takes a list of timeslots and a room number as parameters, and inserts each timeslot into the bookings table in the database.
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    try:
        for timeslot in timeslots:
            cursor.execute("INSERT INTO bookings (Time, RoomNO, Day) VALUES (?, ?, ?)", (timeslot, room, date))
        conn.commit()
    except Exception as e:
        print('Error inserting booking:', e)
    finally:
        conn.close()

@app.route('/submit_booking', methods=['POST']) #This function is used to handle a POST request when a user submits a booking form. It takes the room number and timeslot from the form data, generates a fake booking ID and user ID, and inserts these into the bookings table in the database.
def submit_booking():
    try:
        data = request.get_json()
        timeslots = data.get('timeslots')
        room = data.get('Room')
        date = data.get('date')

        insert_booking(timeslots, room, date)

        return jsonify({'message': 'Booking submitted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True) #debug=True means that the server will reload itself each time you make a change to the code
