from flast import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return 'This is sample text for our web solution'

if __name__ == '__main__':
    app.run()