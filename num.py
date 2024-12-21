import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import random
import time
import os


bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)


def is_user_banned(user_id):
    return user_id in banned_users
banned_users = []

game_active = False
number = None
max_attempts = 3
attempts = 0
active_player_id = None
from datetime import datetime

@bot.message_handler(commands=['start'])
def handle_start(message):
    current_time = datetime.now()
    message_time = datetime.fromtimestamp(message.date) 
    time_difference = (current_time - message_time).total_seconds()
    if time_difference > 20:
        return 

    if message.from_user.id in banned_users:
        bot.reply_to(message, "عذرا , انت محظور من استخدام البوت.")
        bot.reply_to(message, "☝️")
        return

    bot.reply_to(
        message,
        "أهلاً حياك الله! \n"
        "• أرسل `كتويت` لبدء أسئلة الكت تويت. \n"
        "• أرسل /num لبدء لعبة الأرقام.\n"
        "• أرسل `لطمية` ل ارسال لطمية \n"
        "• أرسل `ميم` او `ميمز` للميمز. \n\n"
        " استمتع! 🎉",
        parse_mode='Markdown'
    )
@bot.message_handler(commands=['num'])
def start(message):
    current_time = datetime.now()
    message_time = datetime.fromtimestamp(message.date)  
    time_difference = (current_time - message_time).total_seconds()

    if time_difference > 20:
        return 
    
    if is_user_banned(message.from_user.id):
        send_ban_message(message)
        return
    
    global game_active, attempts, active_player_id
    game_active = False
    attempts = 0
    active_player_id = None
    
    username = message.from_user.username if message.from_user.username else "لا يوجد اسم مستخدم"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ابدأ اللعبة", callback_data="start_game"))
    
    bot.send_video(
        message.chat.id,
        "https://t.me/VIPABH/1204",
        caption=f"أهلاً [{message.from_user.first_name}](https://t.me/{username if message.from_user.username else ''}) حياك الله! اضغط على الزر لبدء اللعبة.",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def start_game(call):
    if is_user_banned(call.from_user.id):
        send_ban_message(call.message)
        return

    global game_active, number, attempts, active_player_id
    if not game_active:
        number = random.randint(1, 10)
        active_player_id = call.from_user.id
        username = call.from_user.username if call.from_user.username else "لا يوجد اسم مستخدم"
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        bot.send_message(
            call.message.chat.id, 
            f"عزيزي [{call.from_user.first_name}](https://t.me/{username if call.from_user.username else ''}) اختر أي رقم من 1 إلى 10 🌚",  
            parse_mode="Markdown"
        )
        game_active = True
        attempts = 0
    else:
        bot.send_message(
            call.message.chat.id, 
            "اللعبة قيد التشغيل، يرجى انتهاء الجولة الحالية أولاً."
        )
def is_user_banned(user_id):
    """التحقق مما إذا كان المستخدم محظورًا."""
    return user_id in banned_users
def send_ban_message(message):
    """إرسال رسالة توضح أن المستخدم محظور."""
    bot.reply_to(message, "عذراً، أنت محظور من استخدام البوت.")
    bot.reply_to(message, "☝️")
    global game_active, number, attempts, active_player_id
    if not game_active:
        number = random.randint(1, 10)
        active_player_id = call.from_user.id
        username = call.from_user.username if call.from_user.username else "لا يوجد اسم مستخدم"

        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        bot.send_message(call.message.chat.id, f'عزيزي  [{call.from_user.first_name}](t.me/@{username}) اختر أي رقم من 1 إلى 10 🌚',  parse_mode="Markdown")
        game_active = True
        attempts = 0
    else:
        bot.reply_to(call.message.chat.id, 'اللعبة قيد التشغيل، يرجى انتهاء الجولة الحالية أولاً.')
        
@bot.message_handler(commands=['ارقام'])
def show_number(message):
    """إظهار الرقم السري عند الطلب وإرساله إلى المسؤول."""
    chat_id = message.chat.id
    target_user_id = 1910015590 
    authorized_users = [1910015590] 
    
    if message.from_user.id not in authorized_users:
        bot.reply_to(message, "عذرًا، لا يمكنك استخدام هذا الامر @k_4x1.")
        return

    if game_active:
        bot.send_message(target_user_id, f"الرقم السري هو: {number}")
        bot.reply_to(message, "تم إرسال الرقم السري إلى @k_4x1.")
    else:
        bot.reply_to(message, "لم تبدأ اللعبة بعد. أرسل '/num' لبدء اللعبة.")
        @bot.message_handler(func=lambda message: game_active and message.from_user.id == active_player_id)
        def handle_guess(message):
            """معالجة التخمينات أثناء اللعبة."""
            global game_active, number, attempts
            if message.from_user.id in banned_users:
                bot.reply_to(message, "عذرًا، أنت محظور من استخدام البوت.")
                return
                try:
                    guess = int(message.text)
                    if guess < 1 or guess > 10:
                        bot.reply_to(message, "يرجى اختيار رقم بين 1 و 10 فقط!")
                        return
                        attempts += 1
                        if guess == number:
                            bot.reply_to(message, "🎉 مُبارك! لقد فزت!")
                            won = "https://t.me/VIPABH/2"  # رابط الصوت للفوز
                            bot.send_voice(message.chat.id, won)
                            game_active = False
                        elif attempts >= max_attempts:
                            bot.reply_to(message, f"للأسف، لقد نفدت محاولاتك. الرقم الصحيح هو {number}. 🌚")
                            lose = "https://t.me/VIPABH/23"  # رابط الصوت للخسارة
                            bot.send_voice(message.chat.id, lose)
                                game_active = False
                        else:
                            remaining_attempts = max_attempts - attempts
                            bot.reply_to(message, f"الرقم غير صحيح. حاول مجددًا! لديك {remaining_attempts} محاولة متبقية.")
                except ValueError:
                    bot.reply_to(message, "يرجى إدخال رقم صحيح بين 1 و 10.")

@bot.message_handler(func=lambda message: message.text in ['ميم', 'ميمز'])
def send_random_file(message):
    time.sleep(2)
    rl = random.randint(2, 255)  
    url = f"t.me/iuabh/{rl}" 

    special_videos = [242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]

    if rl in special_videos:
        bot.send_video(message.chat.id, url, caption="😎 يسعد مسائك", reply_to_message_id=message.message_id)
    else:
        try:
            bot.send_photo(message.chat.id, url, caption="😎 يسعد مسائك", reply_to_message_id=message.message_id)
        except Exception as e:
            bot.reply_to(message, "عذرًا، حدث خطأ أثناء إرسال الملف. جرب مرة أخرى.")

       
questions = [
    "شلون تعمل هالشي؟",
    "شلون تقضي وقتك بالفراغ؟",
    "شلون تتحكم بالضغط؟",
    "شلون تكون صبور؟",
    "شلون تحافظ على التركيز؟",
    "شلون تكون قوي نفسياً؟",
    "شلون تسيطر على الغضب؟",
    "شلون تدير وقتك بشكل فعال؟",
    "شلون تكون ناجح في حياتك المهنية؟",
    "شلون تطور مهاراتك الشخصية؟",
    "شلون تدير الضغوطات في العمل؟",
    "شلون تدير الامور المالية؟",
    "شلون تتعلم لغة جديدة؟",
    "شلون تكون مبدع في عملك؟",
    "شلون تطور علاقاتك الاجتماعية؟",
    "شلون تتغلب على التحديات؟",
    "شلون تنظم حياتك بشكل منظم؟",
    "شلون تحافظ على صحتك؟",
    "شلون تحمي نفسك من الإجهاد؟",
    "شلون تعتني بنفسك بشكل جيد؟",
    "شلون تكون متفائل في الحياة؟",
    "شلون تدير الوقت بين العمل والحياة الشخصية؟",
    "شلون تتعامل مع الشكوك والتوتر؟",
    "شلون تعطي قيمة لوقتك؟",
    "شلون تدير التوتر في العلاقات العائلية؟",
    "شلون تتعلم من الاخطاء؟",
    "شلون تدير الصعوبات في الحياة؟",
    "شلون تكون منظم في حياتك اليومية؟",
    "شلون تحسن من تركيزك وانتباهك؟",
    "شلون تطور مهاراتك الشخصية والاجتماعية؟",
    "شلون تدير العمل في فريق؟",
    "شلون تحسن من قدراتك التواصلية؟",
    "شلون تكون منظم في الدراسة؟",
    "شلون تكون فعال في استخدام التكنولوجيا؟",
    "شلون تحافظ على توازنك بين العمل والحياة الشخصية؟",
    "شلون تتعلم مهارات جديدة بسرعة؟",
    "شلون تكون ملهماً للآخرين؟",
    "شلون تدير الخلافات في العمل؟",
    "شلون تكون مؤثراً في العروض التقديمية؟",
    "شلون تحسن من قدراتك التفكير الإبداعي؟",
    "شلون تطور قدراتك القيادية؟",
    "شلون تكون متفائل في ظروف صعبة؟",
    "شلون تدير التحولات في الحياة؟",
    "شلون تتعلم من النجاحات والإخفاقات؟",
    "شلون تكون مستعداً للتغيير؟",
    "شلون تستمتع بالحياة؟",
    "شلون تكون إنساناً محبوباً ومحترماً؟",
    "شلون تتعلم من خبرات الآخرين؟",
    "شلون تطور مهاراتك في التعلم الذاتي؟",
    "شلون تحسن من قدراتك على اتخاذ القرارات؟",
    "شلون تكون مبادراً في العمل؟",
    "شلون تطور مهاراتك في حل المشكلات؟",
    "شلون تستفيد من النقد البناء؟",
    "شلون تطور ثقتك بالنفس؟",
    "شلون تتعامل مع التغييرات في العمل؟",
    "شلون تطور مهاراتك في التعاون والعمل الجماعي؟",
    "شلون تتعامل مع الضغوطات في الحياة؟",
    "شلونك؟",
    "شنو اسمك؟",
    "شنو جنسيتك؟",
    "شنو عمرك؟",
    "شنو لونك المفضل؟",
    "شنو طبخة تحبها اكثر؟",
    "شنو هوايتك المفضلة؟",
    "شنو مكان سفرة اللي تحلم تروحله؟",
    "شنو نوع السيارة اللي تفضلها؟",
    "شنو نوع الموسيقى اللي تحب تستمع لها؟",
    "شنو تحب تسوي في وقت الفراغ؟",
    "شنو اكلتك المفضلة في الفطور؟",
    "شنو اكلتك المفضلة في الغدا؟",
    "شنو اكلتك المفضلة في العشا؟",
    "شنو نوع الشاي اللي تحب تشربه؟",
    "شنو نوع القهوة اللي تحب تشربها؟",
    "شنو اكثر شيء مميز في ثقافة العراق؟",
    "شنو نوع الافلام اللي تحب تشوفها؟",
    "شنو البلدة العربية اللي تفضل تزورها؟",
    "شنو نوع الهدية اللي تحب تتلقاها؟",
    "شنو اهم شيء بالنسبة إليك في الصداقة؟",
    "شنو الشيء اللي تشوفه عند العراقيين بشكل خاص؟",
    "شنو الاكلة العراقية المفضلة عندك؟",
    "شنو نوع الرياضة اللي تحب تمارسها؟",
    "شنو مكان العراقي اللي تحب تزوره في العراق؟",
    "شنو اكثر شيء تحبه في الطبيعة؟",
    "شنو اللون اللي يحبه العراقيين كثير؟",
    "شنو الشيء اللي يستفزك بسرعة؟",
    "شنو الشيء اللي يخليك تفرح؟",
    "شنو الشيء اللي تحس إنه اكثر شيء يعبر عن الهوية العراقية؟",
    "شنو نوع الهاتف اللي تستخدمه؟",
    "شنو الشيء اللي تحس فيه إنه مفقود في المجتمع العراقي؟",
    "شنو اكثر مكان تحب تزوره في العراق؟",
    "شنو النصيحة اللي تحب تعطيها لشخص صغير؟",
    "شنو الشيء اللي يخليك تشعر بالراحة والهدوء؟",
    "شنو الشيء اللي تحب تسويه بالعطلة؟",
    "شنو الحيوان اللي تحبه اكثر؟",
    "شنو الشيء اللي تحب تهديه لشخص عزيز عليك؟",
    "شنو الشيء اللي تحس بإنجاز كبير إذا قمت به؟",
    "شنو اكثر موقع التواصل الاجتماعي اللي تستخدمه؟",
    "شنو الشيء اللي يحبه العراقيين في الاعياد والمناسبات؟",
    "شنو الشيء اللي تحب تشوفه في العراق مطور ومتطور؟",
    "شنو الشيء اللي تحب تشاركه مع الآخرين بشكل كبير؟",
    "شنو اكثر موسم تحبه في العراق؟",
    "شنو الشيء اللي تتمنى تغيره في العراق؟",
    "شنو الشيء اللي تحب تستثمر فيه وقتك وجهدك؟",
    "شنو الشيء اللي يميز العراق والعراقيين برايك؟",
    "شنو نوع الفن اللي تحب تستمتع به؟",
    "شنو الشيء اللي تحب تتعلمه في المستقبل؟",
    "شنو اكثر شيء تحبه في الشتاء؟",
    "شنو الشيء اللي يرفع معنوياتك بشكل سريع؟",
    "شنو الشيء اللي تحب تهديه لنفسك؟",
    "شنو الشيء اللي تتمنى تحققه في حياتك؟",
     "منو افضل صديق عندك؟",
    "منو شخصيتك المفضلة في الافلام؟",
    "منو الشخص اللي تحب تسافر معه؟",
    "منو الشخص اللي بتستشيره في قراراتك؟",
    "منو اكثر شخص تحب تشوفه كل يوم؟",
    "منو اكثر شخص غريب بتعرفه؟",
    "منو الشخص اللي تحب تحجي معه لساعات؟",
    "منو اكثر شخص قدوة بحياتك؟",
    "منو الشخص اللي تثق فيه بشكل كامل؟",
    "منو اكثر شخص ملهم في حياتك؟",
    "منو الشخص اللي تتمنى تشوفه اليوم؟",
    "منو الشخص اللي تحب تكون جارك؟",
    "منو الشخص اللي بتتحدث معه كل يوم؟",
    "منو الشخص اللي بتشتاقله كثير؟",
    "منو الشخص اللي بتعتمد عليه في الصعوبات؟",
    "منو الشخص اللي تحب تشاركه اسرارك؟",
    "منو الشخص اللي بتقدر قيمته في حياتك؟",
    "منو الشخص اللي تحب تطلب منه المشورة؟",
    "منو الشخص اللي تحب تكون معه في المشاكل؟",
    "منو الشخص اللي بتحسه اكثر شخص يفهمك؟",
    "منو الشخص اللي تحب تحتفل معه في الاعياد؟",
    "منو الشخص اللي تتوقعه اكثر شخص بيرحل عنك؟",
    "منو الشخص اللي تحب تشترك معه في الهوايات؟",
    "منو الشخص اللي تحب تشوفه بعد غياب طويل؟",
    "منو الشخص اللي تتمنى تقدمله هدية مميزة؟",
    "منو الشخص اللي تحب تذهب معه في رحلة استكشافية؟",
    "منو الشخص اللي تحب تحجي معه عن مشاكلك العاطفية؟",
    "منو الشخص اللي تتمنى تكون له نفس قدراتك ومهاراتك؟",
    "منو الشخص اللي تحب تقابله وتشتغل معه في المستقبل؟",
    "منو الشخص اللي تحب تحتفل معه بنجاحك وإنجازاتك؟",
    "منو الشخص اللي بتتذكره بكل سعادة عندما تراجع صورك القديمة؟",
    "منو الشخص اللي تحب تشاركه تجاربك ومغامراتك في الحياة؟",
    "منو الشخص اللي تحب تسمع نصائحه وتطبقها في حياتك؟",
    "منو الشخص اللي تحب تشوفه ضحكته بين الفينة والاخرى؟",
    "منو الشخص اللي تعتبره اكثر شخص يدعمك ويحفزك على تحقيق اهدافك؟",
    "منو الشخص اللي تحب تشوفه محقق نجاحاته ومستقبله المشرق؟",
    "منو الشخص اللي تحب تشكره على وجوده في حياتك ودعمه المستمر؟",
    "منو الشخص اللي تحب تقدمله هدية تذكارية لتخليك تذكره للابد؟",
    "منو الشخص اللي تحب تشكره على دعمه الكبير لك في مشوارك الدراسي؟",
    "منو الشخص اللي تتمنى تعرفه في المستقبل وتصير صداقتكم مميزة؟",
    "منو الشخص اللي تحب تشاركه لحظات الفرح والسعادة في حياتك؟",
    "منو الشخص اللي تعتبره اكثر شخص يستحق منك كل الحب والاحترام؟",
    "منو الشخص اللي تحب تشاركه اسرارك وتحجي له كل شيء بدون تردد؟",
    "منو الشخص اللي تتمنى تحضر معه حفلة موسيقية لفرقتك المفضلة؟",
    "منو الشخص اللي تحب تتنافس معه في لعبة او رياضة تحبها؟",
    "منو الشخص اللي تحب تشوفه مبتسماً ومتفائلاً في الحياة؟",
    "شوكت تفتح المحل؟",
    "شوكت بتروح على العمل؟",
    "شوكت تكون مستعد للمقابلة؟",
    "شوكت بتنوم بالليل؟",
    "شوكت بتصحى بالصبح؟",
    "شوكت بتسافر؟",
    "شوكت بتعود من العمل؟",
    "شوكت بتعمل رياضة؟",
    "شوكت بتذاكر للامتحان؟",
    "شوكت بتنظف البيت؟",
    "شوكت بتقرا الكتاب؟",
    "شوكت تكون فاضي للتسوق؟",
    "شوكت بتنطر الباص؟",
    "شوكت بتعود من السفر؟",
    "شوكت بتشتري الهدية؟",
    "شوكت بتتقابل مع صديقك؟",
    "شوكت بتحضر الحفلة؟",
    "شوكت بتتعشى؟",
    "شوكت بتتناول الفطور؟",
    "شوكت بتسافر في العطلة؟",
    "شوكت بترجع للمنزل؟",
    "شوكت تخلص المشروع؟",
    "شوكت بتتخرج من الجامعة؟",
    "شوكت بتبدا العمل؟",
    "شوكت بتفتح المحل؟",
    "شوكت تنتهي الدورة التدريبية؟",
    "شوكت بتتزوج؟",
    "شوكت بترتب الغرفة؟",
    "شوكت تتعلم الموسيقى؟",
    "شوكت بترتب الوثائق؟",
    "شوكت بتسجل في النادي الرياضي؟",
    "شوكت تستلم الطلبية؟",
    "شوكت بتشوف الطبيب؟",
    "شوكت بتتناول الغداء؟",
    "شوكت تكون مستعد للسفر؟",
    "شوكت بتكمل المشروع؟",
    "شوكت تخلص الواجب؟",
    "شوكت تحصل على النتيجة؟",
    "شوكت تتعلم اللغة الجديدة؟",
    "شوكت بتحضر المؤتمر؟",
    "شوكت بتنهي الكتاب؟",
    "شوكت بتفتح المطعم؟",
    "شوكت بتسافر في الإجازة؟",
    "شوكت بتبدا التدريب؟",
    "شوكت تخلص المشروع الفني؟",
    "شوكت تنتهي الجلسة؟",
    "شوكت تتعلم الطبخ؟",
    "شوكت تستلم الشهادة؟",
    "شوكت بتبدا الرحلة؟",
    "شوكت بتنهي الاعمال المنزلية؟",
    "شوكت تكون فاضي للقراءة؟",
    "شوكت تستلم السيارة الجديدة؟",
    "شوكت بتتناول العشاء؟",
    "وين رايح؟",
    "وين تسكن؟",
    "وين بتشتغل؟",
    "وين بتروح في ايام العطلة؟",
    "وين تحب تسافر في العطلات؟",
    "وين تحب تروح مع الاصدقاء؟",
    "وين تكون في الساعة الثامنة صباحاً؟",
    "وين تكون في الساعة العاشرة مساءً؟",
    "وين تحب تتناول الإفطار؟",
    "وين تحب تتسوق؟",
    "وين تحب تتناول العشاء؟",
    "وين تكون في الساعة الثانية ظهراً؟",
    "وين تحب تمضي امسياتك؟",
    "وين تحب تقضي ايام العطلة؟",
    "وين تحب تزور المعالم السياحية؟",
    "وين تحب تشتري الهدايا؟",
    "وين تحب تتمرن وتمارس الرياضة؟",
    "وين تحب تذهب للتسوق؟",
    "وين تحب تقضي وقتك مع العائلة؟",
    "وين تكون في الساعة الخامسة مساءً؟"
]

@bot.message_handler(func=lambda message: message.text in ['كتويت'])
def send_random_question(message):
    random_question = random.choice(questions)
    bot.reply_to(message, random_question)


basimurl = (
    "50", "51", "52", "53", "54", "55", "56", "57", "58", "59",
    "60", "61", "62", "63", "64", "65", "66", "67", "68", "69",
    "70", "71", "72", "73", "74", "75", "76", "77", "78", "79",
    "80", "81", "82", "83", "84", "85", "86", "87", "88", "89",
    "90", "91", "92", "93", "94", "95", "96", "97", "98", "99",
    "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
    "110", "111", "112", "113", "114", "115", "116", "117", "118"
)

mohmurl = (
    "119", "120", "121", "122", "123", "124", "125", "126", "127", "128",
    "129", "130", "131", "132", "133", "134", "135", "136", "137", "138"
)

musurl = ('139', '140', '141', '142', '143', '144', '145', '146', '147',
            '148', '149', '150', '151', '152', '153', '154'
            )

nurl = ('164', '165', '166', '167', '168', '169', '170')

furl = ('171', '172', '173', '174')


def send_audio_from_list(call, url_list):
    rl = random.choice(url_list)  
    audio_url = f"https://t.me/sossosic/{rl}"  
    
    bot.send_audio(
        chat_id=call.message.chat.id,
        audio=audio_url,
        caption="᯽︙اذكر القائم",
        parse_mode="html"
    )

@bot.message_handler(func=lambda message: message.text in ['لطمية'] or message.text in ['لطميه'])
def vipabh(message):
    current_time = datetime.now()
    message_time = datetime.fromtimestamp(message.date) 
    time_difference = (current_time - message_time).total_seconds()
    if time_difference > 20:
        return 
    username = message.from_user.username if message.from_user.username else "لا يوجد اسم مستخدم"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("باسم", callback_data="باسم"))
    markup.add(types.InlineKeyboardButton("الخاقاني", callback_data="الخاقاني"))
    markup.add(types.InlineKeyboardButton("مسلم", callback_data="مسلم"))
    markup.add(types.InlineKeyboardButton("نزلة", callback_data="نزلة"))
    markup.add(types.InlineKeyboardButton("فاقد", callback_data="فاقد"))
    
    bot.send_video(
        message.chat.id,
        "https://t.me/VIPABH/1212",  
        caption=f"اهلا [{message.from_user.first_name}](https://t.me/{username}) حياك الله! اضغط على الرادود.",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "باسم")
def send_basim(call):
    send_audio_from_list(call, basimurl)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

@bot.callback_query_handler(func=lambda call: call.data == "الخاقاني")
def send_khaqani(call):
    send_audio_from_list(call, mohmurl)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

@bot.callback_query_handler(func=lambda call: call.data == "مسلم")
def send_mus(call):
    send_audio_from_list(call, musurl)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

@bot.callback_query_handler(func=lambda call: call.data == "نزلة")
def send_n(call):
    send_audio_from_list(call, nurl)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

@bot.callback_query_handler(func=lambda call: call.data == "فاقد")
def send_f(call):
    send_audio_from_list(call, furl)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

try:
    bot.polling(none_stop=True, interval=0, timeout=120)
except Exception as e:
    print(f"حدث خطأ: {e}")
    time.sleep(5)
