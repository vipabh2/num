from telethon import TelegramClient, events
import os
import random

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('new_bot_session', api_id, api_hash).start(bot_token=bot_token)

# قائمة الردود المحتملة
abh = [
    "ها",
    "شرايد",
    "تفظل",
    "قُل",
    "😶",
    "https://t.me/VIPABH/1214"
]

# إنشاء العميل

# الاستماع للرسائل الجديدة
@client.on(events.NewMessage(func=lambda e: e.text and ('مخفي' in e.text.strip().lower() or 'المخفي' in e.text.strip().lower())))
async def reply(event):
    vipabh = random.choice(abh)  # اختيار رد عشوائي
    if vipabh.startswith("http"):
        # إرسال رسالة بصوت إذا كان الرد هو رابط
        await event.reply(vipabh, file=vipabh)
    else:
        # إرسال الرد النصي
        await event.reply(vipabh)

# تشغيل العميل
client.run_until_disconnected()
