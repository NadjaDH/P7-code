from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("Home.html")

@app.route('/booking')
def booking():
    return render_template("BookRoom.html")

@app.route('/contact')
def contact():
    return render_template("Contact.html")

@app.route('/information')
def information():
    return render_template("Information.html")

if __name__ == '__main__':
    app.run()

#def GroupRoom()
   # room_number
    #is_avaliable
    #booking_status