from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
from telethon import events
import os
from datetime import datetime

# جلب بيانات البوت من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء العميل الأساسي
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# متغير لحفظ وقت الحظر
user_ban_times = {}

# حدث لكشف التقييد
@client.on(events.UserUpdate)
async def user_update_handler(event):
    if event.user_id and event.is_banned:
        # إذا كان المستخدم قد تم تقييده، نرسل إشعارًا
        user_id = event.user_id
        # يمكن تغيير هذه الرسالة لتتناسب مع أسلوبك
        ban_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        ban_message = f"تم تقييد المستخدم {user_id} في {ban_time}."
        
        # استخراج معرّف المجموعة من الحدث (إذا تم التقييد داخل مجموعة معينة)
        # ملاحظة: في حالة `UserUpdate` قد لا يتوفر `event.chat_id`
        # يمكن حل هذه المشكلة عن طريق مراقبة التفاعل داخل مجموعة ما (استخدام حدث NewMessage)
        if hasattr(event, 'chat_id'):
            group_username = event.chat_id  # إذا كان event يحتوي على معرّف المجموعة
            await client.send_message(group_username, ban_message)

        # حفظ وقت الحظر (إذا أردت حفظه لاستخدامات لاحقة)
        user_ban_times[user_id] = ban_time

async def get_users_without_write_permission(event):
    group_username = event.chat_id  # الحصول على معرف المجموعة من الحدث

    # جلب المشاركين المحظورين فقط باستخدام العميل الأساسي
    participants = await client(GetParticipantsRequest(
        channel=group_username,
        filter=ChannelParticipantsBanned(q=""),  # استخدم قيمة فارغة بدلاً من None
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
        
        # نبحث عن وقت الحظر الفعلي من خلال `banned_until`
        banned_user = next((b for b in participants.users if b.id == user.id), None)
        
        if banned_user and hasattr(banned_user, 'banned_until') and banned_user.banned_until:
            # حفظ تاريخ ووقت الحظر عند التقييد
            user_ban_times[user.id] = banned_user.banned_until.strftime("%Y-%m-%d %I:%M:%S %p")  # حفظ تاريخ ووقت الحظر بتنسيق 12 ساعة
            ban_time = user_ban_times[user.id]  # استخدام الوقت المحفوظ
        else:
            ban_time = "لا يوجد وقت محدد للحظر"

        await event.reply(f"User: {user.id} - {mention}\nBanned Time: {ban_time}", parse_mode="md")

# تشغيل الكود عبر حدث
@client.on(events.NewMessage(pattern='/get_banned'))  # تشغيل الكود عند كتابة الأمر /get_banned
async def handle_event(event):
    await get_users_without_write_permission(event)

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
