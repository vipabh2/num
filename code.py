from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def get_users_without_write_permission(event):
    group_username = event.chat_id 
    participants = await client(GetParticipantsRequest(
        channel=group_username,
        filter=ChannelParticipantsBanned(q=""), 
        offset=0,
        limit=100,
        hash=0
    ))

    if not participants.users:
        await event.reply("لا يوجد مستخدمون محظورون في هذه المجموعة.")
        return
        mention = f"[@{user_to_restrict.username}](https://t.me/{user_to_restrict.username})" if user_to_restrict.username else f"[{user_to_restrict.first_name}](tg://user?id={user_to_restrict.id})"

    for user in participants.users:
        await event.reply(f"User: {user.id} - {mention}", parse_mode="md")

from telethon import events

@client.on(events.NewMessage(pattern='/get_banned')) 
async def handle_event(event):
    await get_users_without_write_permission(event)

client.run_until_disconnected()
