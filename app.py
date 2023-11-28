from flask import Flask, render_template
from accordion import accordion_function
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

@app.route('/information')
def information():
    return render_template("Information.html")

@app.route('/contact')
def contact():
    return render_template("Contact.html")

if __name__ == '__main__':
    app.run()

#def GroupRoom()
   # room_number
    #is_avaliable
    #booking_status