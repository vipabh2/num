from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import GetParticipantRequest

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)

restricted_users = [] 
unmute_permissions = ChatBannedRights(until_date=None, send_messages=False) 

@client.on(events.NewMessage(pattern="/مسح_المقيدين"))
async def unmute(event):
    global restricted_users
    user_id = event.sender_id
    chat_id = event.chat_id

    participant = await client(GetParticipantRequest(chat_id, user_id))
    if (
        participant.participant.admin_rights
        or participant.participant.rank
        or user_id in [5675627801, 5651614955]
    ):
        count = len(restricted_users)

        for user in restricted_users:
            await client.edit_permissions(chat_id, user.id, send_messages=True)

        restricted_users = []  # إعادة تعيين القائمة
        await event.reply(f"↢ تم مسح {count} من المقيدين")
    else:
        await event.reply(f"حجي هذا الامر ليس لك \n༄")

@client.on(events.NewMessage(pattern="المق"))
async def get_restr_users(event):
    global restricted_users
    count = len(restricted_users)

    if count == 0:
        await event.reply("لا يوجد مستخدمين مقيدين.")
        return

    user_ids = [str(user.id) for user in restricted_users]
    response = f"قائمة المقيدين وعددهم: {count}\n"
    response += "⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴀ♪\n"
    response += "\n".join(f"{i+1}. {user_id}" for i, user_id in enumerate(user_ids))

    await event.reply(response)

client.run_until_disconnected()
