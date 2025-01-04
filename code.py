from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
import os

# جلب بيانات البوت من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء العميل الأساسي
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def get_users_without_write_permission(event):
    group_username = event.chat_id  # الحصول على معرف المجموعة من الحدث

    # جلب المشاركين المحظورين فقط باستخدام العميل الأساسي
    participants = await client(GetParticipantsRequest(
        channel=group_username,
        filter=ChannelParticipantsBanned(q=""),  # قيمة فارغة للـ q بدلاً من None
        offset=0,
        limit=100,  # جلب أول 100 مستخدم محظور
        hash=0
    ))

    # إذا لم يكن هناك مشاركون محظورون
    if not participants.users:
        await event.reply("لا يوجد مستخدمون محظورون في هذه المجموعة.")
        return

    # إرسال النتائج للمستخدم الذي أرسل الأمر
    for user in participants.users:
        # إذا كان للمستخدم اسم مستخدم
        mention = f"[@{user.username}](https://t.me/@{user.username})" if user.username else f"[{user.first_name}](tg://user?id={user.id})"
        
        # نبحث عن وقت الحظر (وقت الحظر هو وقت الحظر الفعلي في تاريخ الحظر)
        banned_user = next((b for b in participants.users if b.id == user.id), None)

        # إذا كان هناك وقت حظر فعلي (ليس المدة) من خلال `banned_until`
        if banned_user:
            # إذا كان الحظر دائمًا أو مؤقتًا (المستخدم محظور لوقت محدد)
            ban_time = banned_user.date.strftime("%Y-%m-%d %H:%M:%S")  # وقت الحظر الفعلي
        else:
            ban_time = "لا يوجد وقت محدد للحظر"

        await event.reply(f"User: {user.id} - {mention}\nTime Banned: {ban_time}", parse_mode="md")

# تشغيل الكود عبر حدث
from telethon import events

@client.on(events.NewMessage(pattern='/get_banned'))  # تشغيل الكود عند كتابة الأمر /get_banned
async def handle_event(event):
    await get_users_without_write_permission(event)

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
