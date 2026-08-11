import telebot
from telebot import types
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_data = {}

PRICES = {"all_fb": 2900, "usa_fb": 3500, "all_wa": 4000, "usa_wa": 5000}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🌍 All Countries Facebook - N2900", callback_data="product_all_fb"),
        types.InlineKeyboardButton("🇺🇸 USA Facebook - N3500", callback_data="product_usa_fb"),
        types.InlineKeyboardButton("🌍 All Countries WhatsApp - N4000", callback_data="product_all_wa"),
        types.InlineKeyboardButton("🇺🇸 USA WhatsApp - N5000", callback_data="product_usa_wa")
    )
    bot.send_message(message.chat.id, "👋 Welcome to SMSvirtual!\n\nSelect a number package:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def product_selected(call):
    product = call.data.replace("product_", "")
    user_data[call.from_user.id] = {"product": product}
    bot.send_message(call.message.chat.id, "📧 Please enter your email address:")
    bot.register_next_step_handler(call.message, get_email)

def get_email(message):
    user_id = message.from_user.id
    user_data[user_id]["email"] = message.text
    product = user_data[user_id]["product"]
    price = PRICES[product]
    name = product.replace("_", " ").title()
    summary = f"✅ Order Summary:\n\nPackage: {name}\nEmail: {message.text}\nPrice: N{price}\n\nReply 'PAY' to confirm payment."
    bot.send_message(message.chat.id, summary)

@bot.message_handler(func=lambda message: message.text.upper() == 'PAY')
def payment(message):
    bot.send_message(message.chat.id, "💳 Payment instructions sent to your email!\n\nWe will deliver your number within 5 minutes.")

print("Bot is running on Render...")
bot.polling(none_stop=True)
