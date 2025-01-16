from telethon import TelegramClient, events, Button
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# إعدادات قاعدة البيانات
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# إنشاء مصنع الجلسات في SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# تعريف جدول الهمسات
class Whisper(Base):
    __tablename__ = "whispers"
    whisper_id = Column(String, primary_key=True, index=True)
    sender_id = Column(String)
    username = Column(String)
    message = Column(String)

Base.metadata.create_all(bind=engine)

# إعدادات البوت
api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# دوال قاعدة البيانات
def store_whisper(whisper_id, sender_id, username, message):
    db = SessionLocal()
    try:
        db_whisper = Whisper(whisper_id=whisper_id, sender_id=str(sender_id), username=username, message=message)
        db.add(db_whisper)
        db.commit()
    except Exception as e:
        db.rollback()  # التراجع عن العمليات إذا حدث خطأ
        print(f"حدث خطأ أثناء إضافة الهمسة: {e}")
    finally:
        db.close()

def get_whisper(whisper_id):
    db = SessionLocal()
    try:
        whisper = db.query(Whisper).filter(Whisper.whisper_id == whisper_id).first()
        return whisper
    except Exception as e:
        print(f"حدث خطأ أثناء استرجاع الهمسة: {e}")
    finally:
        db.close()

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text.strip()

    if query: 
        parts = query.split(' ')
        if len(parts) >= 2: 
            message = ' '.join(parts[:-1]) 
            username = parts[-1] 
            
            # التحقق مما إذا كان الإدخال هو ID رقمي أو اسم مستخدم
            if username.isdigit():
                username = username  # إذا كان الإدخال أرقام فقط، اعتبره ID رقمي
            else:
                if not username.startswith('@'):
                    username = f'@{username}'  # إذا لم يبدأ بـ @، أضفه

            try:
                whisper_id = f"{event.sender_id}:{username}"  # إنشاء معرف فريد للهمسة

                # تخزين الهمسة في قاعدة البيانات
                store_whisper(whisper_id, event.sender_id, username, message)

                # إنشاء رسالة الهمسة مع زر
                result = builder.article(
                    title='اضغط لإرسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى \n الله يثخن اللبن عمي ({username})",
                    buttons=[Button.inline(text='tap to see', data=f'send:{username}:{message}:{event.sender_id}:{whisper_id}')]
                )
            except Exception as e:
                result = builder.article(
                    title='خطأ أثناء إنشاء الهمسة',
                    description="حدث خطأ أثناء إنشاء الهمسة.",
                    text=f'حدث خطأ أثناء إنشاء الهمسة: {str(e)}'
                )
        else:
            result = builder.article(
                title='خطأ في التنسيق',
                description="يرجى استخدام التنسيق الصحيح: @username <message>",
                text='التنسيق غير صحيح، يرجى إرسال الهمسة بالتنسيق الصحيح: @username <message>'
            )
        await event.answer([result])

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        _, username, message, sender_id, whisper_id = data.split(':', 4)
        try:
            # استرجاع الهمسة من قاعدة البيانات
            whisper = get_whisper(whisper_id)

            if whisper:
                # التأكد من أن الذي يضغط الزر هو نفس المرسل أو المرسل إليه
                if f"@{event.sender.username or event.sender_id}" == username or str(event.sender_id) == sender_id:
                    await event.answer(f"{whisper.message}", alert=True)
                else:
                    await event.answer("هذه الرسالة ليست موجهة لك!", alert=True)
            else:
                await event.answer("لم يتم العثور على الهمسة!", alert=True)

        except Exception as e:
            await event.answer(f'حدث خطأ: {str(e)}', alert=True)

# استمرار الاتصال بالبوت
client.run_until_disconnected()
