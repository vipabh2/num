from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)


async def get_users_without_write_permission(event):
    group_username = event.chat_id  # الحصول على معرف المجموعة من الحدث
    async with TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token) as client:
        # جلب المشاركين المحظورين فقط
        participants = await client(GetParticipantsRequest(
            channel=group_username,
            filter=ChannelParticipantsBanned(),  # جلب المستخدمين المحظورين فقط
            offset=0,
            limit=100,  # جلب أول 100 مستخدم محظور
            hash=0
        ))

        # طباعة النتائج
        for user in participants.users:
            print(f"User: {user.id} - {user.username} - {user.first_name}")

# تشغيل الكود عبر حدث
from telethon import events


@client.on(events.NewMessage(pattern='/get_banned'))  # تشغيل الكود عند كتابة الأمر /get_banned
async def handle_event(event):
    await get_users_without_write_permission(event)

client.run_until_disconnected()
