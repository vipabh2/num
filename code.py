from telethon import TelegramClient, events, Button
from models import add_or_update_user, add_point_to_winner, get_user_score
from memes import get_link, add_link, delete_link
from bs4 import BeautifulSoup
import requests
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

@bot.on(events.NewMessage(pattern=r"ميمز (\S+) (.+)"))
async def Hussein(event):
    url = event.pattern_match.group(1)
    lMl10l = event.pattern_match.group(2)
    add_link(lMl10l, url)  
    ABH = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    ABH = Get(ABH)
    try:
        await event.client.send_message(event.chat_id, "تم إضافة البصمة بنجاح")
    except BaseException:
        pass

@bot.on(events.NewMessage(pattern=r"\?(.*)"))
async def Hussein(event):
    lMl10l = event.pattern_match.group(1)
    url = get_link(lMl10l)
    if url:
        await event.client.send_file(event.chat_id, url, parse_mode="html")
        await event.delete()

@bot.on(events.NewMessage(pattern="ازالة(?:\s|$)([\s\S]*)"))
async def delete_alClient(event):
    lMl10l = event.pattern_match.group(1)
    delete_link(lMl10l)
    ABH = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    ABH = Get(ABH)
    try:
        await event.client.send_message(event.chat_id, f"تم حذف البصمة '{lMl10l}' بنجاح")
    except BaseException:
        pass

@bot.on(events.NewMessage(pattern="قائمة الميمز"))
async def list_alClient(event):
    links = SESSION.query(AljokerLink).all()
    if links:
        message = "**قائمة الميمز:**\n"
        for link in links:
            message += f"- {link.key}: {link.url}\n"
    else:
        message = "**لاتوجد بصمات ميمز مخزونة حتى الآن**"
    await event.client.send_message(event.chat_id, message)

@bot.on(events.NewMessage(pattern="ازالة_البصمات"))
async def delete_all_alClient(event):
    SESSION.query(AljokerLink).delete()
    await event.client.send_message(event.chat_id, "تم حذف جميع بصمات الميمز")


if __name__ == "__main__":
    while True:
        try:
            # print("✨ بدء تشغيل العميل...")
            Client.start()
            # print("✅ العميل يعمل الآن!")
            Client.run_until_disconnected()
        except Exception as e:
            print(f"⚠️ حدث خطأ: {e}")
            print("⏳ إعادة المحاولة بعد 5 ثوانٍ...")
            time.sleep(5)

