from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Hello from Render!</h1>
    <p>Your deployment works successfully.</p>
    <button onclick="alert('Button works!')">Click Me</button>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)