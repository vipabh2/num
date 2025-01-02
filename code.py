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


print("البوت قيد التشغيل...")
while True:
    try:
        client.run_until_disconnected()
    except Exception as e:
        print(f"حدث خطأ في التشغيل الرئيسي: {e}")
        time.sleep(5)
