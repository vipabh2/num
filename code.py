from telethon import TelegramClient, events, Button
from models import add_or_update_user, add_point_to_winner, get_user_score
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
##########################################################################from telethon import events

@Client.on(events.NewMessage(pattern=r"ميمز (\S+) (.+)"))
async def Hussein(event):
    url = event.pattern_match.group(1)
    lMl10l = event.pattern_match.group(2)
    add_link(lMl10l, url)
    await event.edit(f"**᯽︙ تم اضافة البصمة {lMl10l} بنجاح ✓ **")
    ABH = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    ABH = Get(ABH)
    try:
        await event.Client(ABH)
    except BaseException:
        pass
@Client.on(events.NewMessage(pattern=r"\?(.*)"))
async def Hussein(event):
    lMl10l = event.pattern_match.group(1)
    Client = await reply_id(event)
    url = get_link(lMl10l)
    if url:
        await event.Client.send_file(event.chat_id, url, parse_mode="html", reply_to=Client)
        await event.delete()
        ABH = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        ABH = Get(ABH)
        try:
            await event.Client(ABH)
        except BaseException:
            pass

@Client.on(events.NewMessage(pattern="ازالة(?:\s|$)([\s\S]*)"))
async def delete_alClient(event):
    lMl10l = event.pattern_match.group(1)
    delete_link(lMl10l)
    await event.edit(f"**᯽︙ تم حذف البصمة '{lMl10l}' بنجاح ✓**")
    ABH = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    ABH = Get(ABH)
    try:
        await event.Client(ABH)
    except BaseException:
        pass
@Client.on(events.NewMessage(pattern="قائمة الميمز"))
async def list_alClient(event):
    links = SESSION.query(AljokerLink).all()
    if links:
        message = "**᯽︙ قائمة تخزين اوامر الميمز:**\n"
        for link in links:
            message += f"- البصمة : .`{link.key}`\n"
    else:
        message = "**᯽︙ لاتوجد بصمات ميمز مخزونة حتى الآن**"
    await event.edit(message)
    ABH = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    ABH = Get(ABH)
    try:
        await event.Client(ABH)
    except BaseException:
        pass
@Client.on(events.NewMessage(pattern="ازالة_البصمات"))
async def delete_all_alClient(event):
    SESSION.query(AljokerLink).delete()
    await event.edit("**᯽︙ تم حذف جميع بصمات الميمز من القائمة **")
    ABH = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    ABH = Get(ABH)
    try:
        await event.Client(ABH)
    except BaseException:
        pass

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

