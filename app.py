import uuid
import logging
import os
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import multiprocessing
from database import insert_user_link, get_user_id_by_uuid
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

# Set up logging for bot
logging.basicConfig(level=logging.INFO)

# Flask route
@app.route('/')
def home():
    return 'Go to the bot and generate a link.'

@app.route('/link/<uuid>', methods=['GET'])
def get_user_link(uuid):
    user_id = get_user_id_by_uuid(uuid)
    if user_id:
        return jsonify({'user_id': user_id})
    return jsonify({'error': 'Invalid link'}), 404

# Telegram bot handler
async def create(update: Update, context: CallbackContext):
    user_id = update.message.from_user.name
    unique_id = str(uuid.uuid4()) 
    logging.info(f"Received /create command from user: {user_id}")
    insert_user_link(user_id, unique_id)
    link = f"http://localhost:5000/link/{unique_id}"
    await update.message.reply_text(f"Your unique link is: {link}")

def run_telegram_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("create", create))
    application.run_polling()

def run_flask_server():
    app.run(debug=True, use_reloader=False) 
    
if __name__ == "__main__":
    bot_process = multiprocessing.Process(target=run_telegram_bot)
    bot_process.start()

    flask_process = multiprocessing.Process(target=run_flask_server)
    flask_process.start()

    bot_process.join()
    flask_process.join()
