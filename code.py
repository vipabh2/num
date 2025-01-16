from telethon import TelegramClient, events
import random

api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"

# إنشاء البوت
bot = TelegramClient('b', api_id, api_hash).start(bot_token=bot_token)

# قائمة الأسئلة والإجابات
questions_and_answers = [
    {"question": "ما هو عاصمة العراق؟", "answer": "بغداد"},
    {"question": "ما هو أعلى جبل في العالم؟", "answer": "إفرست"},
    {"question": "كم عدد الكواكب في النظام الشمسي؟", "answer": "8"},
    {"question": "ما هو البحر الذي يفصل بين أوروبا وإفريقيا؟", "answer": "البحر المتوسط"}
]

# تتبع حالة المستخدمين والأسئلة الحالية
user_states = {}

# عندما يرسل المستخدم /start
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    # اختيار سؤال عشوائي
    question = random.choice(questions_and_answers)
    user_states[user_id] = {
        "question": question,
        "waiting_for_answer": True  # وضع المستخدم في انتظار الإجابة
    }
    await event.reply(f"مرحباً {event.sender.first_name}! 🌟\nسأطرح عليك سؤالاً:\n\n{question['question']}")

# مراقبة الإجابات
@bot.on(events.NewMessage)
async def check_answer(event):
    user_id = event.sender_id
    user_message = event.text.strip().lower()

    # التحقق إذا كان المستخدم في وضع الإجابة
    if user_id in user_states and user_states[user_id]["waiting_for_answer"]:
        current_question = user_states[user_id]["question"]
        correct_answer = current_question['answer'].lower()

        if user_message == correct_answer:
            await event.reply("🎉 إجابة صحيحة! ممتاز!")
            del user_states[user_id]  # إزالة حالة المستخدم بعد الإجابة الصحيحة


# تشغيل البوت
print("Bot is running...")
bot.run_until_disconnected()
