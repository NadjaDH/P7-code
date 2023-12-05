from calendar import FRIDAY, MONDAY, THURSDAY, TUESDAY, WEDNESDAY
from flask import Flask, render_template
from accordion import accordion_function, shuffled_function, weekend_function
app = Flask(__name__)

@app.route('/')
def home():
    room_data = accordion_function()
    room_numbers = [4118, 4119, 4120, 4121, 4122]
    room_info = [{'room': room_number, 'status': status} for room_number, status in zip(room_numbers, room_data)]
    
#   day_data = weekend_function()
#   day_date = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]
#   day_info = [{'day' : day_date, 'value': value} for day_date, value in zip(day_data, day_date)]

    mixed_data = shuffled_function()
    index_to_randomize = 2
    mixed_numbers = shuffled_function(index_to_randomize)
    mixed_info = [{'day': mixed_numbers, 'value': value} for mixed_numbers, value in zip(mixed_numbers, mixed_data)]
    return render_template("home.html", room_info=room_info, mixed_info=mixed_info)

@app.route('/booking')
def booking():
    return render_template("BookRoom.html")

@app.route('/information')
def information():
    return render_template("Information.html")

if __name__ == '__main__':
    app.run()

#def GroupRoom()
   # room_number
    #is_avaliable
    #booking_status