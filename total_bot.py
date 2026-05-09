import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from calculation_logic import parse_betting_line, calculate_total_amount, format_output

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid getting too much debug information
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Replace with your actual bot token
import os
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message on /start."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I\'m a betting calculation bot. Send me your betting lines."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message on /help."""
    await update.message.reply_text("Send me your betting lines and I will calculate the total amount.")

async def handle_betting_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the betting message and replies with the calculated total."""
    user_name = update.effective_user.first_name
    betting_text = update.message.text

    # Split the message into individual betting lines
    betting_lines = betting_text.strip().split('\n')

    total_overall_amount = 0
    cashback_percent = 0.0
    cashback_key = None
    
    # Store parsed data for each line to calculate overall cashback correctly
    parsed_lines_data = []

    for line in betting_lines:
        if line.strip(): # Process non-empty lines
            parsed_data = parse_betting_line(line)
            parsed_lines_data.append(parsed_data)
            total_overall_amount += calculate_total_amount(parsed_data)
            
            # If a cashback is found in any line, use it. Assuming one cashback per message.
            if parsed_data["cashback_key"] and not cashback_key:
                cashback_key = parsed_data["cashback_key"]
                cashback_percent = parsed_data["cashback_percent"]

    if total_overall_amount > 0:
        reply_message = format_output(user_name, total_overall_amount, cashback_percent, cashback_key)
        await update.message.reply_text(reply_message)
    else:
        await update.message.reply_text("I couldn\'t understand your betting lines. Please try again with a valid format.")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot\'s token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command messages - handle the betting lines
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_betting_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
  
if __name__ == "__main__":
    main()
