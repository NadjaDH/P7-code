from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/book_room')
def book_room():
    return render_template("booking.html")

if __name__ == '__main__':
    app.run()

#def GroupRoom()
   # room_number
    #is_avaliable
    #booking_status