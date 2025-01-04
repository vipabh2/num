from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
from telethon import events
import os
from datetime import datetime

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

user_ban_times = {}

حدث لكشف التقييد
@client.on(events.UserUpdate)
async def user_update_handler(event):
    try:
        if event.user_id and event.is_banned:
            user_id = event.user_id
            ban_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            print(ban_time)

            user_ban_times[user_id] = ban_time 
            print(user_ban_times)

            if hasattr(event, 'chat_id'):
                group_username = event.chat_id 
                await client.send_message(group_username, f"تم تقييد المستخدم {user_id} في {ban_time}.")
    except Exception as e:
        print(f"Error occurred while updating user ban: {e}")


client.run_until_disconnected()
