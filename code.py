from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)

# قائمة المستخدمين المقيدين
restricted_users = []

# إعداد صلاحيات إلغاء التقييد
unmute_permissions = ChatBannedRights(until_date=None, send_messages=None)

# --- أمر كتم المستخدم ---
@client.on(events.NewMessage(pattern="/كتم"))
async def mute_user(event):
    if event.is_group:
        if not event.reply_to_msg_id:
            await event.reply("⌔ يجب الرد على رسالة المستخدم الذي تريد كتمه.")
            return
        reply_message = await event.get_reply_message()
        user = await client.get_entity(reply_message.sender_id)

        # إضافة المستخدم إلى قائمة المقيدين
        restricted_users.append(user.id)

        # كتم المستخدم
        await client.edit_permissions(
            event.chat_id,
            user.id,
            send_messages=False
        )
        await event.reply(f"✅ ¦ تم كتم المستخدم بنجاح\n{user.mention}")

# --- أمر مسح المقيدين ---
@client.on(events.NewMessage(pattern="/مسح_المقيدين"))
async def unmute_users(event):
    global restricted_users
    count = len(restricted_users)

    # إلغاء التقييد لجميع المستخدمين في القائمة
    for user_id in restricted_users:
        await client.edit_permissions(
            event.chat_id,
            user_id,
            send_messages=True
        )
    restricted_users.clear()  # مسح القائمة
    await event.reply(f"↢ تم مسح {count} من المقيدين")

# --- أمر عرض قائمة المقيدين ---
@client.on(events.NewMessage(pattern="/المقيدين"))
async def get_restricted_users(event):
    global restricted_users
    count = len(restricted_users)

    # التحقق إذا كانت القائمة فارغة
    if count == 0:
        await event.reply("⌔ لا يوجد مستخدمون مقيدون.")
        return

    # إعداد الرد
    user_list = "\n".join([f"- {user_id}" for user_id in restricted_users])
    response = f"⌔ قائمة المقيدين وعددهم: {count}\n\n{user_list}"
    await event.reply(response)

# تشغيل البوت
client.run_until_disconnected()
