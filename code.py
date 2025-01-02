from models import add_or_update_user, add_point_to_winner, get_user_score
import telebot
from telebot import types
import telebot.types
from bs4 import BeautifulSoup
import requests
import random
import time
from datetime import datetime
import os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)


user_id_to_delete = 1910015590
bot_id_to_delete = 793977288

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage)
async def delete_user_messages(event):
    if event.sender_id == user_id_to_delete and "/send" in event.raw_text:
        try:
            await event.delete()
            print(f"تم حذف الرسالة من المستخدم {user_id_to_delete} بنجاح.")
        except Exception as e:
            print(f"حدث خطأ أثناء محاولة حذف الرسالة: {e}")

@client.on(events.NewMessage)
async def delete_other_bots_messages(event):
    if event.sender_id != client.me.id:
        try:
            sender = await event.get_sender()
            if sender.bot: 
                await event.delete()
                print(f"تم حذف رسالة البوت {event.sender_id}.")
        except Exception as e:
            print(f"حدث خطأ أثناء محاولة حذف رسالة البوت: {e}")

print("البوت قيد التشغيل...")
while True:
    try:
        client.run_until_disconnected()
    except Exception as e:
        print(f"حدث خطأ في التشغيل الرئيسي: {e}")
        time.sleep(5)
