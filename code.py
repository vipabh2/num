from telethon import TelegramClient, events
from telethon.tl.types import ChatActionUserRestricted
import os
import logging
from datetime import datetime

# جلب بيانات البوت من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# إعداد السجل (logger)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@client.on(events.ChatAction)
async def handler(event):
    try:
        # تحقق من إذا كان الحدث هو "تقييد" (مستخدم تم تقييده)
        if isinstance(event.action, ChatActionUserRestricted):
            user_id = event.user.id  # استخراج ID المستخدم
            user = await client.get_entity(user_id)
            username = user.username if user.username else user.first_name
            ban_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")  # حفظ وقت الحظر

            # طباعة البيانات لتتبعها
            print(f"User ID: {user_id}")
            print(f"Username: {username}")
            print(f"Ban Time: {ban_time}")

            # تسجيل البيانات في السجل
            logger.info(f"تم تقييد المستخدم {username} (ID: {user_id}) في {ban_time}")

            # إرسال رسالة إلى نفس المجموعة التي تم فيها التقييد
            group_username = event.chat_id
            ban_message = f"تم تقييد المستخدم {username} (ID: {user_id}) في {ban_time}."
            print(f"Sending message to group {group_username}: {ban_message}")
            await client.send_message(group_username, ban_message)
    
    except Exception as e:
        # تسجيل الأخطاء في السجل
        logger.error(f"حدث خطأ أثناء تنفيذ الإجراء: {str(e)}")
        print(f"Error: {str(e)}")  # طباعة الخطأ

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
