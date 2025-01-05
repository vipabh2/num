from telethon import TelegramClient, events
from telethon.tl.types import ChatPermissions
import os

# جلب بيانات البوت من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# حدث لمراقبة التغييرات في حالة المستخدم داخل المجموعة
@client.on(events.ChatAction)
async def action_handler(event):
    try:
        if event.user_added:
            print(f"تم إضافة المستخدم {event.user_id} إلى المجموعة {event.chat_id}")
        elif event.user_kicked:
            print(f"تم إزالة المستخدم {event.user_id} من المجموعة {event.chat_id}")
        elif event.user_restricted:
            print(f"تم تقييد المستخدم {event.user_id} في المجموعة {event.chat_id}")
        
    except Exception as e:
        print(f"حدث خطأ في مراقبة التغييرات: {str(e)}")

# حدث لتقييد مستخدم (تعديل الأذونات)
@client.on(events.NewMessage(pattern='/restrict'))
async def restrict_user(event):
    try:
        if event.chat_id:
            # معرّف المستخدم الذي سيتم تقييده
            user_id = event.reply_to_msg_id  # مثال لتقييد المستخدم المرسل للرسالة السابقة
            chat_id = event.chat_id  # معرّف المجموعة

            # الأذونات التي نريد تعيينها (مثال: منع الكتابة)
            permissions = ChatPermissions(
                send_messages=False,  # منع إرسال الرسائل
                send_media=False,     # منع إرسال الوسائط
                send_stickers=False,  # منع إرسال الملصقات
                send_games=False,     # منع إرسال الألعاب
                send_inline=False,    # منع إرسال الروابط المباشرة
                embed_links=False,    # منع إدراج الروابط
            )

            # تعديل الأذونات
            await client.edit_permissions(chat_id, user_id, permissions)

            # إشعار بخصوص التقييد
            await event.reply(f"تم تقييد المستخدم {user_id} في هذه المجموعة.")
    
    except Exception as e:
        # التعامل مع الأخطاء
        await event.reply(f"حدث خطأ: {str(e)}")

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
