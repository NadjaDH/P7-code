import random
import sqlite3 

# Connect to out database
conn=sqlite3.connect('booking.db')

# Create a cursor  
cursor=conn.cursor()

#execute a sql command
cursor.execute("SELECT * FROM bookings")

def accordion_function():
    room_4118 = True
    room_4119 = True
    room_4120 = True
    room_4121 = True
    room_4122 = True

    roomnumber_list = [room_4118, room_4119, room_4120, room_4121, room_4122] # an array with the bools above
    print(roomnumber_list)
    return roomnumber_list

accordion_function()

