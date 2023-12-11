from flask import Flask, render_template, request, redirect, url_for, jsonify
from accordion import accordion_function
import sqlite3
from dateutil.parser import parse
import traceback


app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('booking.db')
    c = conn.cursor()
    c.execute("SELECT RoomNO, MAX(status) FROM bookings GROUP BY RoomNO")
    room_info = [{'room': room, 'status': bool(status)} for room, status in c.fetchall()]
    conn.close()
    return render_template("home.html", room_info=room_info)

@app.route('/booking')
def booking():
    conn = sqlite3.connect('booking.db')
    c = conn.cursor()
    c.execute("SELECT Time, RoomNO, Day FROM bookings WHERE is_booked = 1") 
    booking_info = [{'room': room, 'time': time, 'date': date,} for room, time, date in c.fetchall()] 
    conn.close()
    # Define selected_date and room
    selected_date = '2022-12-10'  # Replace with actual date
    room = 1  # Replace with actual room number
    return render_template("BookRoom.html", booking_info=booking_info, selected_date=selected_date, room=room)

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

@app.route('/contact')
def contact():
    return render_template("Contact.html")


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

# Update the 'check_in_room' and 'check_out_room' functions as follows

def check_in_room(roomNumber):
    try:
        conn = sqlite3.connect('booking.db')
        c = conn.cursor()

        # Update the status of the room to 'checked in'
        query = "UPDATE bookings SET status = ? WHERE RoomNO = ?"
        params = (False, roomNumber)
        c.execute(query, params)
        print(f"Executing query: {query} with params: {params}")  # Add this line
        conn.commit()
        print(f"checking in room {roomNumber}")
        return True, 'Successfully checked in to room'
    except Exception as e:
        print('Error checking in:', e)
        return False, 'Error checking in to the room'
    finally:
        conn.close()

@app.route('/check_in_room/<roomNumber>', methods=['POST'])
def check_in_route(roomNumber):
    success, message = check_in_room(roomNumber)

    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 500  # Return 500 for server error

def check_out_room(roomNumber):
    print(f"Room number in check_out_room: {roomNumber}")  # Add this line
    try:
    
        conn = sqlite3.connect('booking.db')
    
        # Update the status of the room to 'checked out'
        conn.cursor().execute("UPDATE bookings SET status = ? WHERE RoomNO = ?", (True, roomNumber,)) # Update the status of the room to 'checked out'

        conn.commit() # to update the database
        print(f"checking out room {roomNumber}")
        return True, 'Successfully checked out of room'
    except Exception as e:
        print('Error checking out:', e)
        return False, 'Error checking out of the room'
    finally:
        conn.close()

@app.route('/check_out_room/<roomNumber>', methods=['POST'])
def check_out_route(roomNumber):
    
    success, message = check_out_room(roomNumber)

    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 500  # Return 500 for server error

   

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
