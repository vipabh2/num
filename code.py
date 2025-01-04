from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)
restricted_users = [await client.get_permissions(event.chat_id, user_id)]
@client.on(events.NewMessage(pattern="المقيدين"))
async def list_restricted_users(event):
    global restricted_users

    if not event.is_group:
        await event.reply("⌔ هذا الأمر يعمل فقط في المجموعات.")
        return

    if not restricted_users:
        await event.reply("⌔ لا يوجد أي مستخدمين مقيدين حاليًا.")
        return

    response = "⌔ قائمة المقيدين:\n\n"
    for i, user_id in enumerate(restricted_users, 1):
        try:
            user = await client.get_entity(user_id)
            if user.username:
                mention = f"[{user.first_name}](https://t.me/{user.username})"
            else:
                mention = f"[{user.first_name}](tg://user?id={user.id})"

            response += f"{i}- {mention}\n"
        except Exception as e:
            response += f"{i}- [مستخدم مجهول](tg://user?id={user_id})\n"

    await event.reply(response, parse_mode="md")

# تشغيل البوت
client.run_until_disconnected()
