import uuid
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from database import insert_user_link, get_user_id_by_uuid
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

async def create(update: Update, context: CallbackContext):
    user_id = update.message.from_user.name
    unique_id = str(uuid.uuid4())

    logging.info(f"Received /create command from user: {user_id}")
    insert_user_link(user_id, unique_id)
    uuid_value = get_user_id_by_uuid(user_id)
    link = f"http://localhost:5000/link/{unique_id}"
    await update.message.reply_text(f"Your Unique link is: {link}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("create", create))
    application.run_polling()

if __name__ == "__main__":
    main()
