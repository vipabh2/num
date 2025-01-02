from telethon import TelegramClient, events, Button
from bs4 import BeautifulSoup
import requests
import random
import time
from datetime import datetime
import os
from models import add_or_update_user, add_point_to_winner, get_user_score


api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('new_bot_session', api_id, api_hash).start(bot_token=bot_token)


abh = [
    "ها",
    "شرايد",
    "تفظل",
    "قُل",
    "😶",
    "https://t.me/VIPABH/1214"
]

@client.on(events.NewMessage(func=lambda e: e.text and (e.text.strip().lower().startswith('مخفي') or e.text.strip().lower().startswith('المخفي'))))
async def reply(event):
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await client.send_message(event.chat_id, vipabh, reply_to=event.message.id)
    else:
        await event.reply(vipabh)



print("البوت قيد التشغيل...")
while True:
    try:
        client.run_until_disconnected()
    except Exception as e:
        print(f"حدث خطأ في التشغيل الرئيسي: {e}")
        time.sleep(5)
