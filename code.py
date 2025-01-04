from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
from telethon import events
import os
from datetime import datetime

# جلب بيانات البوت من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء العميل الأساسي
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# متغير لحفظ وقت الحظر
user_ban_times = {}

# حدث لكشف التقييد
@client.on(events.UserUpdate)
async def user_update_handler(event):
    try:
        if event.user_id and event.is_banned:
            user_id = event.user_id
            ban_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            print(ban_time)

            user_ban_times[user_id] = ban_time  # حفظ وقت الحظر
            print(user_ban_times)

            if hasattr(event, 'chat_id'):
                group_username = event.chat_id  # إذا كان event يحتوي على معرّف المجموعة
                await client.send_message(group_username, f"تم تقييد المستخدم {user_id} في {ban_time}.")
    except Exception as e:
        print(f"Error occurred while updating user ban: {e}")


async def get_users_without_write_permission(event):
    try:
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

        for user in participants.users:
            mention = f"[@{user.username}](https://t.me/@{user.username})" if user.username else f"[{user.first_name}](tg://user?id={user.id})"
            ban_info = user_ban_times.get(user.id, {"ban_time": "غير معروف", "first_name": "غير معروف"})
            ban_time = ban_info["ban_time"]
            # print(ban_info)

            first_name = ban_info["first_name"]
            await event.reply(f"User: {first_name} - {mention}\nBanned Time: {ban_time}", parse_mode="md")
    except Exception as e:
        print(f"Error occurred while getting banned users: {e}")

        
# تنفيذ أمر "/get_banned"
@client.on(events.NewMessage(pattern='/get_banned'))
async def handle_event(event):
    try:
        await get_users_without_write_permission(event)
    except Exception as e:
        print(f"Error occurred while executing '/get_banned': {e}")

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
