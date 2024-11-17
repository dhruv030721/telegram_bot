import uuid
import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
URL = os.getenv("SERVER_URL")

# Set up logging
logging.basicConfig(level=logging.INFO)

async def create(update: Update, context: CallbackContext):
    user_id = update.message.from_user.name  # Use 'username' instead of 'name'
    unique_id = str(uuid.uuid4())

    logging.info(f"Received /create command from user: {user_id}")

    # Send POST request with JSON payload
    response = requests.post(
        url=f"{URL}/create_user",
        json={'user_id': user_id, 'uuid': unique_id}
    )

    # Parse the JSON response
    try:
        response_data = response.json()
    except ValueError:
        logging.error("Failed to parse JSON response")
        await update.message.reply_text("Something went wrong!")
        return

    logging.info(f"Response Data: {response_data}")

    if response.status_code == 201:
        link = f"{URL}/link/{unique_id}"
        await update.message.reply_text(f"Your Unique link is: {link}")
    else:
        error_message = response_data.get("message", "Something went wrong!")
        await update.message.reply_text(error_message)

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("create", create))
    application.run_polling()

if __name__ == "__main__":
    main()
