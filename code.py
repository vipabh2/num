from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
from telethon import events
import os
from datetime import datetime
import logging

# جلب بيانات البوت من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء العميل الأساسي
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# حفظ أوقات الحظر للمستخدمين
user_ban_times = {}

# تحديث handler الخاص بالحظر وحفظ الوقت
@client.on(events.UserUpdate)
async def user_update_handler(event):
    try:
        if event.user_id and event.is_banned:
            # إذا كان المستخدم قد تم تقييده
            user_id = event.user_id
            ban_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            ban_message = f"تم تقييد المستخدم {user_id} في {ban_time}."
            
            # استخراج معرّف المجموعة من الحدث
            if hasattr(event, 'chat_id'):
                group_username = event.chat_id
                await client.send_message(group_username, ban_message)

            # حفظ وقت الحظر في القاموس
            user_ban_times[user_id] = {
                "ban_time": ban_time,
                "first_name": event.user.first_name if event.user else "غير معروف"
            }
    except Exception as e:
        error_message = f"حدث خطأ أثناء محاولة تقييد المستخدم {event.user_id}: {str(e)}"
        group_username = 'ID_OF_ADMIN_OR_GROUP'
        await client.send_message(group_username, error_message)
        logger.error(f"Error: {str(e)}")

# جلب المستخدمين المحظورين في المجموعة
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

        # إرسال تفاصيل الحظر لكل مستخدم
        for user in participants.users:
            mention = f"[@{user.username}](https://t.me/@{user.username})" if user.username else f"[{user.first_name}](tg://user?id={user.id})"
            ban_info = user_ban_times.get(user.id, {"ban_time": "غير معروف", "first_name": "غير معروف"})
            ban_time = ban_info["ban_time"]
            first_name = ban_info["first_name"]
            await event.reply(f"User: {first_name} - {mention}\nBanned Time: {ban_time}", parse_mode="md")
    except Exception as e:
        error_message = f"حدث خطأ أثناء جلب المشاركين المحظورين: {str(e)}"
        group_username = 'ID_OF_ADMIN_OR_GROUP'
        await client.send_message(group_username, error_message)
        logger.error(f"Error: {str(e)}")

# أمر لإرجاع المستخدمين المحظورين
@client.on(events.NewMessage(pattern='/get_banned'))
async def handle_event(event):
    try:
        await get_users_without_write_permission(event)
    except Exception as e:
        error_message = f"حدث خطأ أثناء تنفيذ أمر /get_banned: {str(e)}"
        group_username = 'ID_OF_ADMIN_OR_GROUP'
        await client.send_message(group_username, error_message)
        logger.error(f"Error: {str(e)}")

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
