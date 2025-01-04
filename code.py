import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import smtplib
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


token = "7541559770:AAEa6PFRzIMOktbuuTuY8nwfXP2Swn1W99k"  
bot = telebot.TeleBot(token, parse_mode="Markdown")

Owner = 1910015590
BayaTi = set()

user_data = {}
info_updated = {}

start_spam_button = types.InlineKeyboardButton(text="بدء الإرسال", callback_data="start_spam")
view_accounts_button = types.InlineKeyboardButton(text="عرض حسابات", callback_data="view_accounts")
set_email_button = types.InlineKeyboardButton(text="تعيين ايميل", callback_data="set_email")
set_victim_email_button = types.InlineKeyboardButton(text="تعيين ايميلات", callback_data="set_victim_email")
set_message_subject_button = types.InlineKeyboardButton(text="تعيين موضوع", callback_data="set_message_subject")
set_message_button = types.InlineKeyboardButton(text="تعيين كليشة", callback_data="set_message")
set_send_count_button = types.InlineKeyboardButton(text="تعيين عدد إرسال", callback_data="set_send_count")
set_image_button = types.InlineKeyboardButton(text="تعيين صورة", callback_data="upload_image")
set_interval_button = types.InlineKeyboardButton(text="تعيين سليب", callback_data="set_interval")
clear_upload_image_button = types.InlineKeyboardButton(text="مسح صورة الرفع", callback_data="clear_upload_image")
view_info_button = types.InlineKeyboardButton(text="عرض معلوماتك", callback_data="view_info")
clear_info_button = types.InlineKeyboardButton(text="مسح معلوماتك", callback_data="clear_info")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if user_id in BayaTi:
        if user_id not in user_data:
            user_data[user_id] = {
                "accounts": [],
                "victim": [],
                "subject": None,
                "message_body": None,
                "number": None,
                "interval": 4,
                "image_data": None,
                "is_spamming": False,
                "messages_sent_count": 0,
                "messages_failed_count": 0,
                "last_message_id": None,
            }
        if user_id not in info_updated:
            info_updated[user_id] = False
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(start_spam_button)
        markup.add(view_accounts_button, set_email_button)
        markup.add(set_victim_email_button, set_message_subject_button)
        markup.add(set_message_button, set_send_count_button)
        markup.add(set_image_button, set_interval_button)
        markup.add(view_info_button, clear_upload_image_button)
        markup.add(clear_info_button)
        bot.reply_to(message, "اهلا بك في بوت رفع الـ خارجي ( صلخ بلنعال )", reply_markup=markup)
    else:
        bot.reply_to(message, "*• نجب عزيزي ، ارسلت شعار للمالك حتى يوافق عليك ...*")
        request_approval(user_id, message.from_user.username)

def request_approval(user_id, username):
    key = InlineKeyboardMarkup(row_width=1)
    approve_button = InlineKeyboardButton(text="• موافقه •", callback_data=f"Done_{user_id}")
    reject_button = InlineKeyboardButton(text="• رفض الموافقة •", callback_data=f"Reject_{user_id}")
    key.add(approve_button, reject_button)
    bot.send_message(Owner, f'''*• لقد طلب أحدهم لاستخدام البوت 🤡 
• تريد توافق عليه او لا ؟ 🤷🏽‍♂️ ..
- @{username} | {user_id}*''', reply_markup=key)

@bot.callback_query_handler(func=lambda call: call.data.startswith("Done_") or call.data.startswith("Reject_"))
def handle_approval(call):
    user_id = int(call.data.split('_')[1])
    if call.data.startswith('Done_'):
        BayaTi.add(user_id)
        bot.send_message(user_id, "*تم وافقت عليه*")
        bot.send_message(Owner, "*• وافقت عليه ياروع ...*")
    elif call.data.startswith("Reject_"):
        bot.send_message(user_id, "*• ما وافقت عليك ياروع هههههههه...*")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    if user_id not in BayaTi:
        bot.send_message(user_id, "لم يتم الموافقة عليك بعد.")
        return

    if call.data == "set_email":
        bot.send_message(user_id, "أرسل الايميل:رمز تطبيقات")
        bot.register_next_step_handler(call.message, set_email, user_id)

    elif call.data == "set_victim_email":
        bot.send_message(user_id, "أرسل إيميلات الضحايا مفصولة بفواصل")
        bot.register_next_step_handler(call.message, set_victim_email, user_id)

    elif call.data == "set_message_subject":
        bot.send_message(user_id, "أرسل موضوع الرسالة")
        bot.register_next_step_handler(call.message, set_message_subject, user_id)

    elif call.data == "set_message":
        bot.send_message(user_id, "أرسل الكليشة ")
        bot.register_next_step_handler(call.message, set_message, user_id)

    elif call.data == "set_send_count":
        bot.send_message(user_id, "أرسل عدد الرسائل ")
        bot.register_next_step_handler(call.message, set_send_count, user_id)

    elif call.data == "set_interval":
        bot.send_message(user_id, "ارسل الوقت بين رسالة ورسالة بثواني")
        bot.register_next_step_handler(call.message, set_interval, user_id)

    elif call.data == "start_spam":
        user_data[user_id]['is_spamming'] = True
        start_spam(user_id)

    elif call.data == "view_info":
        if info_updated.get(user_id, False):
            bot.send_message(user_id, "تم تحديث المعلومات.")
            info_updated[user_id] = False
        info_text = f"البريد الإلكتروني: {', '.join([account['email'] for account in user_data[user_id]['accounts']])}\nرمز التطبيقات: {', '.join([account['password'] for account in user_data[user_id]['accounts']])}\nموضوع الرسالة: {user_data[user_id]['subject']}\nالرسالة: {user_data[user_id]['message_body']}\nسليب الرسائل: {user_data[user_id]['interval']} ثانية\nعدد الرسائل: {user_data[user_id]['number']}\nمسار الصورة: {'تم رفع الصورة' if user_data[user_id]['image_data'] else 'لم يتم تعيين صورة'}"
        bot.send_message(user_id, info_text)

    elif call.data == "clear_info":
        clear_info(user_id)
        info_updated[user_id] = True
        bot.send_message(user_id, "تم مسح جميع المعلومات.")

    elif call.data == "clear_upload_image":
        clear_uploaded_image(user_id)
        info_updated[user_id] = True
        bot.send_message(user_id, "تم مسح صورة الرفع.")

    elif call.data == "upload_image":
        bot.send_message(user_id, "ارسل الصورة")
        bot.register_next_step_handler(call.message, upload_image, user_id)

    elif call.data == "view_accounts":
        if user_data[user_id]['accounts']:
            accounts_text = "\n".join([f"{account['email']} : {account['password']}" for account in user_data[user_id]['accounts']])
            bot.send_message(user_id, f"الحسابات الموجودة:\n{accounts_text}")
            bot.send_message(user_id, "لحذف حساب، أرسل /cler ايميل:باسورد")
        else:
            bot.send_message(user_id, "لا توجد حسابات مضافة حتى الآن.")

@bot.message_handler(commands=['cler'])
def delete_account(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id]['accounts']:
        try:
            account_info = message.text.split(':')
            if len(account_info) == 2:
                email, password = account_info
                user_data[user_id]['accounts'] = [acc for acc in user_data[user_id]['accounts'] if not (acc['email'] == email and acc['password'] == password)]
                bot.reply_to(message, "تم حذف الحساب.")
            else:
                bot.reply_to(message, "تنسيق غير صحيح، يرجى اتباع التنسيق: ايميل:باسورد")
        except Exception as e:
            bot.reply_to(message, str(e))
    else:
        bot.reply_to(message, "لا توجد حسابات مضافة.")

def set_email(message, user_id):
    email = message.text.strip()
    if user_id not in user_data:
        user_data[user_id] = {"accounts": []}
    user_data[user_id]['accounts'].append({"email": email})
    bot.send_message(user_id, "تم تعيين الايميل.")

def set_victim_email(message, user_id):
    emails = message.text.split(',')
    user_data[user_id]['victim'] = [email.strip() for email in emails]
    bot.send_message(user_id, "تم تعيين إيميلات الضحايا.")

def set_message_subject(message, user_id):
    user_data[user_id]['subject'] = message.text.strip()
    bot.send_message(user_id, "تم تعيين موضوع الرسالة.")

def set_message(message, user_id):
    user_data[user_id]['message_body'] = message.text.strip()
    bot.send_message(user_id, "تم تعيين الكليشة.")

def set_send_count(message, user_id):
    try:
        count = int(message.text.strip())
        user_data[user_id]['number'] = count
        bot.send_message(user_id, "تم تعيين عدد الرسائل.")
    except ValueError:
        bot.send_message(user_id, "يرجى إدخال عدد صحيح.")

def set_interval(message, user_id):
    try:
        interval = int(message.text.strip())
        user_data[user_id]['interval'] = interval
        bot.send_message(user_id, "تم تعيين السليب.")
    except ValueError:
        bot.send_message(user_id, "يرجى إدخال رقم صحيح.")

def clear_info(user_id):
    user_data[user_id] = {
        "accounts": [],
        "victim": [],
        "subject": None,
        "message_body": None,
        "number": None,
        "interval": 4,
        "image_data": None,
        "is_spamming": False,
        "messages_sent_count": 0,
        "messages_failed_count": 0,
        "last_message_id": None,
    }

def clear_uploaded_image(user_id):
    user_data[user_id]['image_data'] = None

def upload_image(message, user_id):
    if message.content_type == 'photo':
        user_data[user_id]['image_data'] = message.photo[-1].file_id
        bot.send_message(user_id, "تم رفع الصورة.")
    else:
        bot.send_message(user_id, "يرجى إرسال صورة فقط.")

def start_spam(user_id):
    if user_data[user_id]['is_spamming']:
        bot.send_message(user_id, "يتم الإرسال بالفعل.")
        return
    user_data[user_id]['is_spamming'] = True
    bot.send_message(user_id, "بدأ الإرسال...")

    email = user_data[user_id]['accounts'][0]['email']
    password = user_data[user_id]['accounts'][0]['password']
    victim_emails = user_data[user_id]['victim']
    subject = user_data[user_id]['subject']
    message_body = user_data[user_id]['message_body']
    number_of_messages = user_data[user_id]['number']
    interval = user_data[user_id]['interval']

    for _ in range(number_of_messages):
        try:
            send_email(email, password, victim_emails, subject, message_body)
            user_data[user_id]['messages_sent_count'] += 1
        except Exception as e:
            user_data[user_id]['messages_failed_count'] += 1
            bot.send_message(user_id, f"خطأ أثناء الإرسال: {str(e)}")
        sleep(interval)

    bot.send_message(user_id, f"تم إرسال {user_data[user_id]['messages_sent_count']} رسالة بنجاح.")
    user_data[user_id]['is_spamming'] = False

def send_email(sender_email, sender_password, recipient_emails, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

bot.infinity_polling()
