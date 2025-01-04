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
        filter=ChannelParticipantsBanned(q=""),  # تمرير سلسلة فارغة كاستعلام
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
        
        # نبحث في المشاركين المحظورين للحصول على وقت الحظر
        banned_until = None
        for banned_user in participants.banned:
            if banned_user.user_id == user.id:
                banned_until = banned_user.date
                break

        # استخراج وقت الحظر (في حالة وجوده)
        if banned_until:
            ban_time = banned_until.strftime("%Y-%m-%d %H:%M:%S")  # تنسيق الوقت بشكل مناسب
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
