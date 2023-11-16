from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

<<<<<<< HEAD
@app.route('/book_room')
def book_room():
=======
@app.route('/booking')
def booking():
>>>>>>> Test
    return render_template("booking.html")

if __name__ == '__main__':
    app.run()

#def GroupRoom()
   # room_number
    #is_avaliable
    #booking_status