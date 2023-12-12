from flask import Flask, render_template, request, redirect, url_for, jsonify
from accordion import accordion_function
import sqlite3
from dateutil.parser import parse
import traceback


app = Flask(__name__)

@app.route('/')
def home():
    #CHAT GPT
    conn = sqlite3.connect('booking.db')
    c = conn.cursor()
    #manually adding a list with room numbers
    all_rooms = ['Room 4.118', 'Room 4.120', 'Room 4.122', 'Room 4.124', 'Room 4.125']
   # Fetch the status for each room from the database
    c.execute("SELECT RoomNO, status FROM bookings")
    room_statuses = dict(c.fetchall())

    # Create room_info list with default status values
    room_info = [{'room': room, 'status': room_statuses.get(room, 'Available')} for room in all_rooms]

    conn.close()
    return render_template("home.html", room_info=room_info)
   # conn = sqlite3.connect('booking.db')
   # c = conn.cursor()
   # c.execute("SELECT DISTINCT RoomNO, status FROM bookings") 
   # room_info = [{'room': room, 'status': status} for room, status in c.fetchall()] 
   # conn.close()
#return render_template("home.html", room_info=room_info)

@app.route('/booking')
def booking():
    conn = sqlite3.connect('booking.db')
    c = conn.cursor()
    c.execute("SELECT StartTime, EndTime, RoomNO, Day FROM bookings WHERE is_booked = 1")
    booking_info = [{'room': room, 'timeslot': f'{start_time} - {end_time}', 'date': date} for room, start_time, end_time, date in c.fetchall()]
    conn.close()
    return render_template("BookRoom.html", booking_info=booking_info, is_timeslot_booked=is_timeslot_booked)

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

@app.route('/is_timeslot_booked', methods=['POST']) #This function is used to handle a POST request when a user submits a booking form. It takes the room number and timeslot from the form data, generates a fake booking ID and user ID, and inserts these into the bookings table in the database.
def is_timeslot_booked_route():
    try:
        data = request.get_json()
        timeslot = data.get('timeslot')
        room = data.get('room')
        date = data.get('date')

        return jsonify({'message': is_timeslot_booked(timeslot, room, date)}), 200
    except ValueError as e: #This exception is raised when a double booking is detected.
        return jsonify({'error': str(e)}), 400 #Return 400 for bad request
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def is_timeslot_booked(timeslot, room, date):
    print(timeslot, room, date)
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    try:
        # Check if there is any booking with the specified timeslot, room, and date
        print(f"timeslot: {timeslot}, room: {room}, date: {date}")
        query = "SELECT COUNT(*) FROM bookings WHERE StartTime <= ? AND EndTime >= ? AND RoomNO = ? AND Day = ? AND is_booked = 1"

        print(query)
        start_time, end_time = timeslot.split(' - ')
        cursor.execute(query, (start_time, end_time, room, date))
        count = cursor.fetchone()[0]

        if count >0:
            raise DoubleBookingError(f"Double booking detected for timeslot {timeslot} on {date} in Room {room}")
        
        return False #Return false if the timeslot is available
    except Exception as e:
        print('Error checking if timeslot is booked:', e)
        return True  # Assume the timeslot is booked in case of an error
    finally:
        conn.close()
        
def from_Timeslots_To_Booking (room, date, timeslots): #Define one booking as one booking only
    bookings = []
    if len(timeslots) > 0:
        lastBookingPosition = -1 #ingen bookinger gemt i liste endnu
        
        for timeslot in timeslots:
            #check list of timeslots
            timeslotTexts =f"{timeslot}".split()
            startTime = timeslotTexts[0]
            endTime = timeslotTexts[2]
            
            #If timeslot startTime er forskellig fra booking endTime så append
            
            # else ret booking endTime til timeslot endTime
            if lastBookingPosition == -1:
                booking = [room, date, startTime, endTime]
                bookings.append(booking)
                lastBookingPosition = lastBookingPosition + 1
            else:
                lastBooking = bookings[lastBookingPosition]
                
                if startTime != lastBooking[3]:
                    booking = [room, date, startTime, endTime]
                    bookings.append(booking)
                    lastBookingPosition = lastBookingPosition + 1
                else:
                    bookings[lastBookingPosition][3] = endTime
                 
                
        for booking in bookings:
            print(f'bookings {booking}')
    return bookings

#TODO:
#def from_bookings_to_Timeslot(bookings):
#    return timeslots, room og date
       
def insert_booking(timeslots, room, date, BookID):
    #OBS: BookID har ingen værdi, men værdi sættes i tabellen ved INSERT
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()
    # Check om brugerens antal bookings er lovlige (Hent users gyldige bookinger ..)
    try:
        # Omsæt timeslots til bookings
        bookings = from_Timeslots_To_Booking( room, date, timeslots  )
        #print(f'BookId {BookID}')
        # Check if the timeslot is already booked
        # (senere) Hent brugerens valide bookinger og check om brugeren samlet set overholder krav
        
        #Slet brugerens nuværende bookings for dette rum og denne dato - de skal overskrives af de nye bookings
        sql = f"DELETE FROM bookings WHERE Day = '{date}' AND RoomNO = '{room}'"
        print(sql)
        cursor.execute(sql)
        
        # Gem bookings i database
        for booking in bookings:
            # Check if the timeslot is already booked
          #TODO:  if is_timeslot_booked(timeslot, room, date):
           #     raise ValueError(f'Timeslot {timeslot} for Room {room} on {date} is already booked.')
           cursor.execute("INSERT INTO bookings (RoomNO, Day, StartTime, EndTime, is_booked) VALUES(?, ?, ?, ?, 1)", (room, date, booking[2], booking[3]))

            # If the timeslot is not booked, insert the booking and set is_booked to 1
            #cursor.execute("INSERT INTO bookings (BookingID, Time, RoomNO, Day, is_booked) VALUES (?, ?, ?, ?, 1)", (BookID, timeslot, room, date))
    
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
