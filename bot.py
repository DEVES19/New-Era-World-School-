from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import json
import os

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 123456789  # replace with your Telegram ID

NAME, CLASS, PHONE = range(3)

menu_keyboard = [
    ["📢 Notices", "📅 Exams"],
    ["💰 Fees", "📝 Admission"],
    ["📞 Contact"]
]
reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

def save_user(user_id):
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump([], f)

    with open("users.json", "r") as f:
        users = json.load(f)

    if user_id not in users:
        users.append(user_id)

    with open("users.json", "w") as f:
        json.dump(users, f)

def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    save_user(user_id)

    update.message.reply_text(
        "🎓 Welcome to New Era World School Bot\n\nChoose an option:",
        reply_markup=reply_markup
    )

def menu_handler(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "📢 Notices":
        update.message.reply_text("📢 School will remain open for administrative work.")

    elif text == "📅 Exams":
        update.message.reply_text("📅 Exams starting soon.")

    elif text == "💰 Fees":
        update.message.reply_text("💰 Please deposit fees before 10th.")

    elif text == "📞 Contact":
        update.message.reply_text("📞 Contact: +91 XXXXX XXXXX")

    elif text == "📝 Admission":
        update.message.reply_text("Enter Student Name:")
        return NAME

    return ConversationHandler.END

def get_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    update.message.reply_text("Enter Class:")
    return CLASS

def get_class(update: Update, context: CallbackContext):
    context.user_data['class'] = update.message.text
    update.message.reply_text("Enter Phone Number:")
    return PHONE

def get_phone(update: Update, context: CallbackContext):
    context.user_data['phone'] = update.message.text

    with open("admissions.json", "a") as f:
        f.write(json.dumps(context.user_data) + "\n")

    update.message.reply_text("✅ Admission submitted!")
    return ConversationHandler.END

def broadcast(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        update.message.reply_text("❌ Not authorized")
        return

    message = " ".join(context.args)

    with open("users.json", "r") as f:
        users = json.load(f)

    for user in users:
        try:
            context.bot.send_message(chat_id=user, text=message)
        except:
            pass

    update.message.reply_text("✅ Broadcast sent!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text("📝 Admission"), menu_handler)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            CLASS: [MessageHandler(Filters.text & ~Filters.command, get_class)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, get_phone)],
        },
        fallbacks=[]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, menu_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
