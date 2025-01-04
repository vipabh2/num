from telethon import TelegramClient, events
from db import add_restricted_user, get_restricted_users  # استيراد وظائف قاعدة البيانات
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)
@client.on(events.NewMessage(pattern="تق"))
async def mute_user(event):
    if not event.is_group:
        await event.reply("⌔ هذا الأمر يعمل فقط في المجموعات.")
        return

    sender = await event.get_sender()
    user_status = await client.get_permissions(event.chat_id, sender.id)

    if user_status.is_admin or sender.id == 5089553588:
        if not event.reply_to_msg_id:
            await event.reply("⌔ يجب الرد على رسالة المستخدم الذي تريد تقيده.")
            return

        reply_message = await event.get_reply_message()
        user_to_restrict = await client.get_entity(reply_message.sender_id)

        if user_to_restrict.id == 5089553588:
            await event.reply("⌔ عذرًا، لا يمكنك تقيد المطور.")
            return

        await client.edit_permissions(event.chat_id, user_to_restrict.id, send_messages=False)

        # إضافة المستخدم إلى قاعدة البيانات أو قائمة المقيدين
        # add_restricted_user(user_to_restrict.id, event.chat_id, user_to_restrict.username, user_to_restrict.first_name, 'سبب التقييد')

        mention = f"[@{user_to_restrict.username}](https://t.me/{user_to_restrict.username})" if user_to_restrict.username else f"[{user_to_restrict.first_name}](tg://user?id={user_to_restrict.id})"
        await event.reply(f"✅ ¦ تم تقيد المستخدم بنجاح: {mention}", parse_mode="md")
    else:
        await event.reply("⌔ ليس لديك صلاحيات لتنفيذ هذا الأمر.")

@client.on(events.NewMessage(pattern="المقيدين"))
async def list_restricted_users(event):
    if not event.is_group:
        await event.reply("⌔ هذا الأمر يعمل فقط في المجموعات.")
        return

    # استرجاع المقيدين من قاعدة البيانات
    restricted_users = get_restricted_users()

    if not restricted_users:
        await event.reply("⌔ لا يوجد أي مستخدمين مقيدين حاليًا.")
        return

    response = "⌔ قائمة المقيدين:\n\n"
    for i, user in enumerate(restricted_users, 1):
        mention = f"[{user[1]}](https://t.me/{user[1]})" if user[1] else f"[{user[2]}](tg://user?id={user[0]})"
        response += f"{i}- {mention} ({user[0]})\n"

    await event.reply(response, parse_mode="md")

client.run_until_disconnected()
