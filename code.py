from telethon import TelegramClient, events
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
        # التحقق إذا كان الإجراء هو "تقييد"
        if event.action == 'restricted':
            user_id = event.user_id
            # الحصول على اسم المستخدم إذا كان موجودًا
            user = await client.get_entity(user_id)
            username = user.username if user.username else user.first_name
            print(username)
            ban_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            print(ban_time)
            logger.info(f"تم تقييد المستخدم {username} (ID: {user_id}) في {ban_time}")
            
            group_username = event.chat_id  # معرّف المجموعة
            print(group_username)
            ban_message = f"تم تقييد المستخدم {username} (ID: {user_id}) في {ban_time}."
            print(ban_message)
            await client.send_message(group_username, ban_message)
    
    except Exception as e:
        # تسجيل الأخطاء في السجل
        logger.error(f"حدث خطأ: {str(e)}")

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
