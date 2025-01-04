import os
try:
    import telebot
    import json 
    import requests
    from telebot import types
    import random
except ImportError:
    os.system("pip install telebot")
    os.system("pip install requests")
from telebot import types
import json
import requests
import random 
token = "7541559770:AAEa6PFRzIMOktbuuTuY8nwfXP2Swn1W99k"  # ضع التوكن الخاص بك هنا
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def s1(mes):
    mar = types.InlineKeyboardMarkup()
    mar.add(types.InlineKeyboardButton(text="def", url="https://t.me/yzzyyzy"))
    bot.reply_to(mes, "اهلا بك في بوت تفاعلات تلقائي", reply_markup=mar)

@bot.message_handler(func=lambda message: True)
def nn(mes):
    reaction = ['😢', '😤', '👿', '😉', '👄', '🫦', '💋']
    em = random.choice(reaction)
    send_message_react({
        'chat_id': mes.chat.id,
        'message_id': mes.message_id,
        'reaction': json.dumps([{'type': 'emoji', 'emoji': em}])
    })

def send_message_react(data={}):
    url = f"https://api.telegram.org/bot{token}/setmess"
    res = requests.post(url, data=data)
    if res.status_code != 200:
        return 'error: ' + res.text
    else:
        return res.json()

bot.infinity_polling()
