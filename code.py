from telethon import TelegramClient, events
import os
import random

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('new_bot_session', api_id, api_hash).start(bot_token=bot_token)

abh = [
    # "ها",
    # "شرايد",
    # "تفظل",
    # "قُل",
    # "😶",
    "https://t.me/VIPABH/1214"
]


@client.on(events.NewMessage(func=lambda e: e.text and ('مخفي' in e.text.strip().lower() or 'المخفي' in e.text.strip().lower())))
async def reply(event):
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await event.reply(file=vipabh)
    else:
        await event.reply(vipabh)

client.run_until_disconnected()
