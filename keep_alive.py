from flask import Flask
app = Flask('')
@app.route('/')
def home():
    return "OK", 200
