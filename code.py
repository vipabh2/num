from telethon import TelegramClient, events, Button
from models import add_or_update_user, add_point_to_winner, get_user_score
from memes import get_link, add_link, delete_link
from bs4 import BeautifulSoup
import requests
import base64
import random
import time
from datetime import datetime
import os
import random
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import InputMediaPhoto
from telethon.tl.custom import Button
#########
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
Client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)
##########################################################################


if __name__ == "__main__":
    while True:
        try:
            # print("✨ بدء تشغيل العميل...")
            Client.start()
            # print("✅ العميل يعمل الآن!")
            Client.run_until_disconnected()
        except Exception as e:
            print(f"⚠️ حدث خطأ: {e}")
            # print("⏳ إعادة المحاولة بعد 5 ثوانٍ...")
            # time.sleep(5)

