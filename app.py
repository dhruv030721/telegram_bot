from flask import Flask, jsonify
from database import init_db, get_user_id_by_uuid

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
