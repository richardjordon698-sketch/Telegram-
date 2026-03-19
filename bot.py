from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# --- Replace with your bot token ---
TOKEN = "8761255230:AAEMUccZ4htDMCjeuJ7G8L2Q_qgGAbQxdNk"

# Store user states & data
user_state = {}
user_data = {}

# --- Start Command ---
def start(update: Update, context: CallbackContext):
    keyboard = [["Cancel Order", "Refund Status", "Contact Support"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text(
        "👋 Welcome to Customer Support\n\nHow can we help you today?",
        reply_markup=reply_markup
    )

# --- Handle Messages ---
def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    text = update.message.text

    # Initialize user
    if user_id not in user_state:
        user_state[user_id] = "menu"
        user_data[user_id] = {}

    # --- Menu चयन ---
    if text == "Cancel Order":
        user_state[user_id] = "cancel_order_id"
        update.message.reply_text("📝 Enter your Order ID:")

    elif user_state[user_id] == "cancel_order_id":
        user_data[user_id]["order_id"] = text
        user_state[user_id] = "cancel_name"
        update.message.reply_text("Enter your Full Name:")

    elif user_state[user_id] == "cancel_name":
        user_data[user_id]["name"] = text
        user_state[user_id] = "cancel_email"
        update.message.reply_text("Enter your Email:")

    elif user_state[user_id] == "cancel_email":
        user_data[user_id]["email"] = text
        user_state[user_id] = "cancel_reason"
        update.message.reply_text("Reason for Cancellation:")

    elif user_state[user_id] == "cancel_reason":
        user_data[user_id]["reason"] = text

        update.message.reply_text(
            "✅ Cancellation request received!\n\nNow proceed to refund form."
        )

        user_state[user_id] = "refund_payment"
        update.message.reply_text("💳 Enter Payment Method (UPI / Bank / Card):")

    # --- Refund Flow ---
    elif user_state[user_id] == "refund_payment":
        user_data[user_id]["payment_method"] = text
        user_state[user_id] = "refund_details"
        update.message.reply_text("Enter Refund Details (UPI ID / Bank Acc / IFSC):")

    elif user_state[user_id] == "refund_details":
        user_data[user_id]["refund_details"] = text
        user_state[user_id] = "refund_amount"
        update.message.reply_text("Enter Amount Paid:")

    elif user_state[user_id] == "refund_amount":
        user_data[user_id]["amount"] = text

        # Final confirmation
        summary = f"""
✅ Refund Request Submitted!

📦 Order ID: {user_data[user_id]['order_id']}
👤 Name: {user_data[user_id]['name']}
💳 Method: {user_data[user_id]['payment_method']}
💰 Amount: {user_data[user_id]['amount']}

⏳ Processing... You’ll be updated soon.
        """

        update.message.reply_text(summary)

        # Reset user state
        user_state[user_id] = "menu"

    else:
        update.message.reply_text("Please choose an option from menu.")

# --- Main Function ---
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()