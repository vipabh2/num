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

from telethon.errors import ChannelPrivateError

# تعديل الوظيفة لإضافة معالجة الأخطاء
async def get_users_without_write_permission(event):
    group_username = event.chat_id  # الحصول على معرف المجموعة من الحدث

    try:
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

    except ChannelPrivateError:
        await event.reply("لا أملك الإذن للوصول إلى هذه القناة أو قد أكون محظورًا فيها.")
        print(f"البوت لا يملك الإذن للوصول إلى القناة {group_username}")
    except Exception as e:
        await event.reply(f"حدث خطأ أثناء جلب المشاركين المحظورين: {str(e)}")
        print(f"Error: {str(e)}")


# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
