from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["restaurant"]
collection = db["invoice"]

# Define a route for the invoice page
@app.route('/invoice/<id>')
def invoice(id):
    # Retrieve the invoice data from MongoDB
    invoice = db.invoice.find_one({"_id": int(id)})
    # Render the HTML template with the invoice data
    return render_template('invoice.html', invoice=invoice)

@app.route("/login", methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    print("Logging in ")
    username = request.json.get("username")
    password = request.json.get("password")
    print(username, password)

    if username == "admin" and password == "password":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)