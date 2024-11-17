from flask import Flask, jsonify, request
from database import init_db, get_user_id_by_uuid, insert_user_link
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Initialize the database
init_db()

@app.route("/")
def home():
    return "Please visit our Telegram bot to get your link."

@app.route("/link/<uuid>")
def user_link(uuid):
    user_id = get_user_id_by_uuid(uuid)
    if user_id:
        return f"Your Telegram user ID is: {user_id}"
    else:
        return "Invalid link or user not found.", 404

# Create User
@app.route("/create_user", methods = ["POST"])
def createUser():
    data = request.get_json() 
    if not data or 'user_id' not in data or 'uuid' not in data:
        return jsonify({"message": "Invalid request data", "status_code": 400}), 400

    user_id = data["user_id"]
    uuid = data["uuid"]
    
    logging.info(f"{user_id} and {uuid}")
    
    # Insert user data into the database
    insert_user_link(user_id, uuid)
    
    return jsonify({"message": "User inserted successfully!", "uuid": uuid}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
