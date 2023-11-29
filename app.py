from flask import Flask, render_template, request, redirect, url_for, jsonify
from accordion import accordion_function
import sqlite3
from dateutil.parser import parse


app = Flask(__name__)

@app.route('/')
def home():
    room_data = accordion_function()
    room_numbers = [4118, 4119, 4120, 4121, 4122]
    room_info = [{'room': room_number, 'status': status} for room_number, status in zip(room_numbers, room_data)]
    return render_template("home.html", room_info=room_info)

@app.route('/booking')
def booking():
    return render_template("BookRoom.html")

def cancel_booking(booking_id):
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    try:
        # Execute a SQL DELETE command to delete the booking with the given booking ID from the bookings table
        cursor.execute("DELETE FROM bookings WHERE BookingID = ?", (booking_id,))

        # If no rows were affected, the booking ID was not found in the database.
        if cursor.rowcount == 0:
            return False, 'Booking ID not found'

        # Commit the changes and close the connection to the database
        conn.commit()
        return True, 'Booking successfully cancelled'
    except Exception as e:
        print('Error cancelling booking:', e)
        return False, 'Error cancelling the booking'
    finally:
        conn.close()

@app.route('/cancel_booking_route', methods=['POST'])
def cancel_booking_route():
    try:
        booking_id = int(request.form.get('booking_id')) #This function is used to handle a POST request when a user submits a booking ID to cancel a booking. It takes the booking ID from the form data and calls the cancel_booking function to delete the booking from the database.

        if not booking_id:
            return jsonify({'error': 'Booking ID is missing in the request'}), 400

        success, message = cancel_booking(booking_id)

        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 404  # Return 404 for not found
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/information')
def information():
    return render_template("Information.html")

class DoubleBookingError(Exception): #This class is used to create a custom exception that is raised when a double booking is detected.
    pass

def is_timeslot_booked(timeslot, room, date):
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    try:
        # Check if there is any booking with the specified timeslot, room, and date
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE Time = ? AND RoomNO = ? AND Day = ?", (timeslot, room, date))
        count = cursor.fetchone()[0]

        if count >0:
            raise DoubleBookingError(f"Double booking detected for timeslot {timeslot} on {date} in Room {room}")
        
        return False #Return false if the timeslot is available
    except Exception as e:
        print('Error checking if timeslot is booked:', e)
        return True  # Assume the timeslot is booked in case of an error
    finally:
        conn.close()

def insert_booking(timeslots, room, date, BookID):
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    try:
        for timeslot in timeslots:
            # Check if the timeslot is already booked
            if is_timeslot_booked(timeslot, room, date):
                raise ValueError(f'Timeslot {timeslot} for Room {room} on {date} is already booked.')

            # If the timeslot is not booked, insert the booking and set is_booked to 1
            cursor.execute("INSERT INTO bookings (BookingID, Time, RoomNO, Day, is_booked) VALUES (?, ?, ?, ?, 1)", (BookID, timeslot, room, date))

        # Commit the changes
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
        BookID = data.get('BookID')

        for timeslot in timeslots:
            if is_timeslot_booked(timeslot, room, date):
                return jsonify({'error': 'One or more selected timeslots are already booked'}), 400
        # Insert the booking into the database if there are no double bookings
        insert_booking(timeslots, room, date, BookID)

        return jsonify({'message': 'Booking submitted successfully'}), 200
    except ValueError as e: #This exception is raised when a double booking is detected.
        return jsonify({'error': str(e)}), 400 #Return 400 for bad request
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True) #debug=True means that the server will reload itself each time you make a change to the code
