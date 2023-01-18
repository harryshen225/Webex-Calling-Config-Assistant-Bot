import requests
import json
from flask import Flask, jsonify

# Create a new Flask app
app = Flask(__name__)

# Define a route for the root URL
@app.route("/")
def index():
    return "Hello, World!"

# Define a route for a JSON endpoint
@app.route("/data")
def data():
    my_data = {"key": "value"}
    return jsonify(my_data)

# Start the app
if __name__ == "__main__":
    app.run(debug=True)
