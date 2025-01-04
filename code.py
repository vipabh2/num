from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)



# تعريف restricted_users كقائمة فارغة في البداية
restricted_users = []  # قائمة المستخدمين المقيدين (ستكون محدثة عند تنفيذ الأوامر)


@client.on(events.NewMessage(pattern="المقيدين"))
async def list_restricted_users(event):
    global restricted_users  # التأكد من أن المتغير عالمي

    # التأكد من أن الحدث جاء من مجموعة
    if not event.is_group:
        await event.reply("⌔ هذا الأمر يعمل فقط في المجموعات.")
        return

    # قائمة للإجابة
    response = "⌔ قائمة المقيدين:\n\n"
    updated_restricted_users = []  # قائمة محدثة للمستخدمين المقيدين

    # التمرير عبر قائمة المستخدمين المقيدين
    for i, user_id in enumerate(restricted_users, 1):
        try:
            # الحصول على صلاحيات المستخدم في المجموعة
            permissions = await client.get_permissions(event.chat_id, user_id)

            # التحقق إذا كان المستخدم مقيدًا من إرسال الرسائل
            if not permissions.send_messages:
                updated_restricted_users.append(user_id)
                user = await client.get_entity(user_id)

                # إذا كان للمستخدم اسم مستخدم (username)
                if user.username:
                    mention = f"[{user.first_name}](https://t.me/{user.username})"
                else:
                    mention = f"[{user.first_name}](tg://user?id={user.id})"

                # إضافة المستخدم إلى قائمة المقيدين
                response += f"{i}- {mention} ({user.id})\n"
            else:
                continue
        except Exception as e:
            # إذا كان هناك خطأ أو لا يمكن الوصول للمستخدم
            response += f"{i}- [مستخدم مجهول](tg://user?id={user_id}) ({user_id})\n"
            print(f"Error: {e}")

    # تحديث قائمة المقيدين
    restricted_users = updated_restricted_users

    # إرسال رد قائمة المقيدين
    if updated_restricted_users:
        await event.reply(response, parse_mode="md")
    else:
        await event.reply("⌔ لا يوجد أي مستخدمين مقيدين حاليًا.")

# قم بتشغيل العميل
client.start()
client.run_until_disconnected()
التعديلات والشرح:
