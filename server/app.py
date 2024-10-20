from flask import Flask

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def getData():
    return "Hello, World!\n"

if __name__ == '__main__':
    app.run(debug=True)
