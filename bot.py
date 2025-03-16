import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ✅ Your bot token from @BotFather
BOT_TOKEN = "7937094956:AAHVDz4y2A2PABntdBeMIfTPp5uD3icMy9w"

# ✅ Your private channel (users must join this)
PRIVATE_CHANNEL = "@gectomovie"
PRIVATE_CHANNEL_LINK = "https://t.me/+GqBXuC5qmXE4NTA1"  # Private channel invite link

# ✅ Your public movie storage channels
CHANNELS = ["@gectomoa"]
    #"@YourPublicChannel2",
    #"@YourPublicChannel3",
    #"@YourPublicChannel4"]

def is_user_joined(update: Update, context: CallbackContext) -> bool:
    """Check if the user is a member of the private channel."""
    user_id = update.message.chat_id
    try:
        chat_member = context.bot.get_chat_member(PRIVATE_CHANNEL, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message and check if the user has joined the private channel."""
    user_id = update.message.chat_id

    if not is_user_joined(update, context):
        keyboard = [[InlineKeyboardButton("Join Now", url=PRIVATE_CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("🚨 You must join our private channel to use this bot!", reply_markup=reply_markup)
        return

    update.message.reply_text("Hello! Send a movie name, and I'll find it for you. 🎬")

def search_movies(update: Update, context: CallbackContext) -> None:
    """Search for movies in the public channels."""
    if not is_user_joined(update, context):
        keyboard = [[InlineKeyboardButton("Join Now", url=PRIVATE_CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("🚨 You must join our private channel to use this bot!", reply_markup=reply_markup)
        return

    query = update.message.text.strip().lower()
    if not query:
        update.message.reply_text("Please enter a movie name.")
        return

    results = []
    for channel in CHANNELS:
        search_query = f"{query} {channel}"
        search_results = context.bot.search_messages(channel, query)

        for msg in search_results:
            if msg.video or msg.document:
                movie_title = msg.caption if msg.caption else "Unknown Movie"
                download_button = InlineKeyboardMarkup([
                    [InlineKeyboardButton("👉👉 Download now 👈👈", url=msg.link)]
                ])
                results.append(f"**Title:** {movie_title}", reply_markup=download_button)

    if results:
        for result in results:
            update.message.reply_text(result)
    else:
        update.message.reply_text("Movie not found. Try a different name!")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_movies))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


