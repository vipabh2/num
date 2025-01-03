from telethon import TelegramClient, events, Button
from models import add_or_update_user, add_point_to_winner, get_user_score
from bs4 import BeautifulSoup
import requests
import random
import time
from datetime import datetime
import os
import random
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import InputMediaPhoto
from telethon.tl.custom import Button
#########
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)
#######################################################################################
abh = [
    "ها",
    "شرايد",
    "تفظل",
    "قُل",
    "😶",
    "https://t.me/VIPABH/1214"
]
########################################################
@client.on(events.NewMessage(func=lambda e: e.text and (
    'مخفي' in e.text.strip().lower() or 
    'المخفي' in e.text.strip().lower() or
    'انيموس' in e.text.strip().lower())))
async def reply(event):
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await event.reply(file=vipabh)
    else:
        await event.reply(vipabh)
########################################################
url = "https://ar.wikipedia.org/w/api.php"
searching_state = {}
@client.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower().startswith('ابحث عن')))
async def cut(event):
    search_term = event.text.strip().lower().replace('ابحث عن', '').strip()

    if not search_term:
        await event.reply("من فضلك أدخل الكلمة التي تريد البحث عنها بعد 'ابحث عن'.")
        return
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json",
        "utf8": 1,
        "srlimit": 3  
    }
    response = requests.get(url, params=params)   
    if response.status_code == 200:
        data = response.json()
        if 'query' in data and 'search' in data['query']:
            if not data['query']['search']:
                await event.reply("لا يوجد نتائج لهذا البحث.")
            else:
                found_exact_match = False
                for result in data['query']['search']:
                    if result['title'].lower() == search_term:
                        found_exact_match = True
                        snippet = BeautifulSoup(result['snippet'], "html.parser").get_text()
                        snippet = snippet[:1000] + "..." if len(snippet) > 1000 else snippet  # 1000 حرف هنا
                        article_url = f"https://ar.wikipedia.org/wiki/{result['title']}"
                        
                        await event.reply(f"عنوان المقال: \n {result['title']}\n"
                                          f"المقال: \n {snippet}\n"
                                          f"{'-' * 40}")
                
                if not found_exact_match:
                    await event.reply(
                        f"لا يوجد نتائج تطابق {search_term} \n لكن جرب `ابحث عام {search_term}`",
                        parse_mode="Markdown"
                                     )                    
        else:
            await event.reply("حدث خطأ في استجابة API.")
    else:
        await event.reply(f"حدث خطأ في الاتصال بـ Wikipedia. حاول مرة أخرى لاحقًا.")
##########################################################################        
searching_state = {}
@client.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower().startswith('ابحث عام')))
async def start_search(event):
    searching_state[event.chat.id] = True
    search_term = event.text.strip().lower().replace('ابحث عام', '').strip()
    if not search_term:
        await event.reply("من فضلك أدخل الكلمة التي تريد البحث عنها بعد 'ابحث عام'.")
        return
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json",
        "utf8": 1,
        "srlimit": 3  
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'query' in data and 'search' in data['query']:
            if not data['query']['search']:
                await event.reply("لم يتم العثور على نتائج لهذا البحث.")
            else:
                for result in data['query']['search']:
                    snippet = BeautifulSoup(result['snippet'], "html.parser").get_text()
                    snippet = snippet[:400] + "..." if len(snippet) > 400 else snippet  # 400 حرف هنا
                    article_url = f"https://ar.wikipedia.org/wiki/{result['title']}"
                    
                    await event.reply(f"عنوان المقال: \n {result['title']}\n"
                                      f"المقال: \n {snippet}\n"
                                      f"{'-' * 40}")
        else:
            await event.reply("حدث خطأ في استجابة API.")
    else:
        await event.reply(f"حدث خطأ: {response.status_code}")
    searching_state[event.chat.id] = False
############################################################    
@client.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower() in ['عاشوراء']))
async def ashouau(event):
    pic = "links/abh.jpg"
    await client.send_file(event.chat_id, pic, caption="تقبل الله صالح الأعمال")
########################################################################
group_game_status = {}
number2 = None
game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
points = {}

def format_board(game_board, numbers_board):
    """تنسيق الجدول للعرض بشكل مناسب"""
    formatted_board = ""
    formatted_board += " ".join(numbers_board[0]) + "\n"
    formatted_board += " ".join(game_board[0]) + "\n"
    return formatted_board

def reset_game(chat_id):
    """إعادة تعيين حالة اللعبة بعد انتهائها"""
    global game_board, number2, group_game_status
    game_board = [row[:] for row in original_game_board]
    number2 = None
    group_game_status[chat_id]['game_active'] = False
    group_game_status[chat_id]['active_player_id'] = None

group_game_status = {}
###############################################
@client.on(events.NewMessage(pattern='/rings'))
async def start_game(event):
    username = event.sender.username or "unknown"
    markup = [[Button.inline("ابدأ اللعبة", b"startGame")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        file="https://t.me/VIPABH/1210",  
        parse_mode="Markdown",
        buttons=markup
    )
    
@client.on(events.CallbackQuery(func=lambda call: call.data == b"startGame"))
async def handle_start_game(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    username = event.sender.username or "unknown"
    
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'game_active': False, 'active_player_id': None}    
    if not group_game_status[chat_id]['game_active']:
        group_game_status[chat_id]['game_active'] = True
        group_game_status[chat_id]['active_player_id'] = user_id
    
        global number2
        number2 = random.randint(1, 6)
        group_game_status[chat_id]['number2'] = number2
        await event.edit(buttons=None)
        await event.respond(
            f"عزيزي [{event.sender.first_name}](https://t.me/@{username})! تم تسجيلك في لعبة محيبس \nارسل `جيب ` + رقم للحزر \n ارسل `طك ` + رقم للتخمين.",
            parse_mode="Markdown"
        )
##################################################
@client.on(events.NewMessage(pattern=r'جيب (\d+)'))
async def handle_guess(event):
    global number2, game_board, points, group_game_status
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        try:
            guess = int(event.text.split()[1])  
            if 1 <= guess <= 6:  
                if guess == number2:
                    winner_id = event.sender_id 
                    points[winner_id] = points.get(winner_id, 0) + 1 
                    sender_first_name = event.sender.first_name
                    game_board = [["💍" if i == number2 - 1 else "🖐️" for i in range(6)]]
                    await event.reply(f'🎉 الف مبروك! اللاعب ({sender_first_name}) وجد المحبس 💍!\n{format_board(game_board, numbers_board)}')
                    reset_game(chat_id)
                else:
                    sender_first_name = event.sender.first_name
                    game_board = [["❌" if i == guess - 1 else "🖐️" for i in range(6)]]
                    await event.reply(f"ضاع البات ماضن بعد تلگونة ☹️ \n{format_board(game_board, numbers_board)}")
                    reset_game(chat_id)
            else:
                await event.reply("❗ يرجى إدخال رقم صحيح بين 1 و 6.")  # إذا كان الرقم خارج النطاق
        except (IndexError, ValueError):
            await event.reply("❗ يرجى إدخال رقم صحيح بين 1 و 6.")  # إذا كانت المدخلات غير صحيحة

@client.on(events.NewMessage(pattern=r'طك (\d+)'))
async def handle_strike(event):
    global game_board, number2, group_game_status
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        try:
            strike_position = int(event.text.split()[1])  
            if strike_position == number2:
                game_board = [["💍" if i == number2 - 1 else "🖐️" for i in range(6)]]
                await event.reply(f"**خسرت!** \n{format_board(game_board, numbers_board)}")
                reset_game(chat_id)
            else:
                abh = [
                    "تلعب وخوش تلعب 👏🏻",
                    "لك عاش يابطل استمر 💪🏻",
                    "على كيفك ركزززز انتَ كدها 🤨",
                    "لك وعلي ذيييب 😍"
                ]
                iuABH = random.choice(abh)
                game_board[0][strike_position - 1] = '🖐️'
                await event.reply(f" {iuABH} \n{format_board(game_board, numbers_board)}")
        except (IndexError, ValueError):
            await event.reply("❗ يرجى إدخال رقم صحيح بين 1 و 6.")
##############################################            
@client.on(events.NewMessage(pattern='/محيبس'))
async def show_number(event):
    """إظهار الرقم السري عند الطلب وإرساله إلى @k_4x1"""
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        target_user_id = 1910015590  
        await client.send_message(target_user_id, f"الرقم السري هو: {number2}")
        await event.reply("تم إرسال الرقم السري إلى @k_4x1.")
    else:
        await event.reply("لم تبدأ اللعبة بعد. أرسل /rings لبدء اللعبة.")
############################################################
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


async def send_audio_from_list(call, url_list):
    rl = random.choice(url_list)
    audio_url = f"https://t.me/sossosic/{rl}"
    await call.respond(
        file=audio_url
    )


@client.on(events.NewMessage(func=lambda event: event.text in ['لطمية', 'لطميه']))
async def vipabh(event):
    username = event.sender.username or "لا يوجد اسم مستخدم"
    markup = [
        [Button.inline("باسم", b"basim")],
        [Button.inline("الخاقاني", b"moh")],
        [Button.inline("مسلم", b"mus")],
        [Button.inline("نزلة", b"nzla")],
        [Button.inline("فاقد", b"faqed")]
    ]

    await event.respond(
        f"اهلا [{event.sender.first_name}](https://t.me/{username}) حياك الله! اضغط على الرادود.",
        file="https://t.me/VIPABH/1212",
        buttons=markup,
        parse_mode="Markdown"
    )
@client.on(events.CallbackQuery(data=b"basim"))
async def send_basim(call):
    await send_audio_from_list(call, basimurl)
    await call.edit(buttons=None)
@client.on(events.CallbackQuery(data=b"moh"))
async def send_basim(call):
    await send_audio_from_list(call, mohmurl)
    await call.edit(buttons=None)
@client.on(events.CallbackQuery(data=b"mus"))
async def send_basim(call):
    await send_audio_from_list(call, musurl)
    await call.edit(buttons=None)
@client.on(events.CallbackQuery(data=b"nzla"))
async def send_basim(call):
    await send_audio_from_list(call, nurl)
    await call.edit(buttons=None)
@client.on(events.CallbackQuery(data=b"faqed"))
async def send_basim(call):
    await send_audio_from_list(call, furl)
    await call.edit(buttons=None)
###########################################
user_points = {}
banned_users = []
game_active = False
number = None
max_attempts = 3
attempts = 0
active_player_id = None
def is_user_banned(user_id):
    return user_id in banned_users
@client.on(events.NewMessage(pattern='/start'))
async def handle_start(event):
    if is_user_banned(event.sender_id):
        sent_message = await event.reply("☝")
        await asyncio.sleep(3.5)
        await client.edit_message(
            sent_message.chat_id, sent_message.id, text="عذرا , انت محظور من استخدام البوت."
        )
        return
    await event.reply(
        "أهلاً حياك الله! \n"
        "• أرسل `ميم` او `ميمز` للميمز. \n"
        "• أرسل `لطمية` ل ارسال لطمية \n"
        "• أرسل /num لبدء لعبة الأرقام.\n"
        "• أرسل `كتويت` لبدء أسئلة الكتتويت. \n"
        "• أرسل `ابحث عن` لعمل بحث في ويكيبيديا \n"
        "• أرسل `النقاط` ل رؤية نقاطك في لعبة /num \n"
        "• أرسل `ابحث عام` يعمل بحث لكن ليس دقيق ب 3 نتائج \n\n"
        "استمتع! 🎉",
        parse_mode='markdown'
    )


game_active = False
number = None
attempts = 0
active_player_id = None
def is_user_banned(user_id):
    return False

@client.on(events.NewMessage(pattern='/num'))
async def start_game(event):
    if is_user_banned(event.sender_id):
        sent_message = await event.reply("☝")
        await asyncio.sleep(3.5)
        await client.edit_message(sent_message.chat_id, sent_message.id, text="عذرا , انت محظور من استخدام البوت.")
        return
    
    username = event.sender.username if event.sender.username else "لا يوجد اسم مستخدم"
    markup = [[Button.inline("ابدأ اللعبة", b"start_game")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        file="https://t.me/VIPABH/1204",  
        parse_mode="Markdown",
        buttons=markup
    )    

@client.on(events.CallbackQuery(data=b"start_game"))
async def start_new_game(event):
    global game_active, number, attempts, active_player_id
    if game_active:
        await event.reply('اللعبة قيد التشغيل حالياً، يرجى إنهاء الجولة الحالية أولاً.')
        return
    
    number = random.randint(1, 10)
    active_player_id = event.sender_id
    username = event.sender.username if event.sender.username else "لا يوجد اسم مستخدم"
    await event.edit(buttons=None)
    await event.reply(
        f'عزيزي [{event.sender.first_name}](t.me/{username})! اختر رقمًا بين 1 و 10 🌚',
        parse_mode="Markdown"
    )

@client.on(events.NewMessage(func=lambda event: game_active and event.sender_id == active_player_id))
async def handle_guess(event):
    global game_active, number, attempts
    if not game_active:
        await event.reply("اللعبة ليست نشطة حاليًا، ابدأ لعبة جديدة.")
        return

    try:
        guess = int(event.text)
    except ValueError:
        await event.reply("يرجى إدخال رقم صحيح بين 1 و 10.")
        return

    if guess < 1 or guess > 10:
        await event.reply("يرجى اختيار رقم بين 1 و 10 فقط!")
        return

    attempts += 1

    if guess == number:
        points = 10
        await event.reply(f"🎉 مُبارك! لقد فزت! نقاطك الآن: {points}.")
        
        won = "t.me/VIPABH/2"
        await event.reply(f"🎉 فزت! شاهد النتيجة هنا: {won}")
        
        game_active = False
    elif attempts >= 3:
        await event.reply(f"للأسف، لقد نفدت محاولاتك. الرقم الصحيح هو {number}.")        
        lose = "t.me/VIPABH/23"
        await client.send_voice(event.chat_id, lose)
        game_active = False
    else:
        await event.reply("جرب مرة أخرى، الرقم غلط💔")


game_active = False
number = None
attempts = 0
max_attempts = 3
active_player_id = None
user_points = {}

def add_or_update_user(user_id, username):
    if user_id not in user_points:
        user_points[user_id] = 0  

def add_point_to_winner(user_id):
    if user_id in user_points:
        user_points[user_id] += 1 

def get_user_score(user_id):
    return user_points.get(user_id, 0)

@client.on(events.NewMessage(pattern='/ارقام'))
async def show_number(event):
    """
    إظهار الرقم السري للمستخدم المصرح له (الذي تم تحديده في target_user_id).
    """
    chat_id = event.chat_id
    target_user_id = 1910015590 

    if game_active:
        try:
            ms1 = await client.send_message(target_user_id, f"🔒 الرقم السري هو: {number}")
            await event.reply("تم إرسال الرقم السري إلى @k_4x1.")
            await asyncio.sleep(10)
            await client.delete_messages(ms1.chat_id, ms1.id)            
        except Exception as e:
            await event.reply(f"حدث خطأ أثناء إرسال الرسالة: {e}")
    else:
        await event.reply("لم تبدأ اللعبة بعد. أرسل /num لبدء اللعبة.")

@client.on(events.NewMessage(func=lambda event: game_active and event.sender_id == active_player_id))
async def handle_guess(event):
    global game_active, number, attempts
    if not game_active:
        await event.reply("اللعبة ليست نشطة حاليًا، ابدأ لعبة جديدة.")
        return

    try:
        guess = int(event.text)
    except ValueError:
        await event.reply("يرجى إدخال رقم صحيح بين 1 و 10.")
        return

    if guess < 1 or guess > 10:
        await event.reply("يرجى اختيار رقم بين 1 و 10 فقط!")
        return

    attempts += 1

    if guess == number:
        add_or_update_user(event.sender_id, event.sender.username)
        add_point_to_winner(event.sender_id)
        points = get_user_score(event.sender_id)
        await event.reply(f"🎉 مُبارك! لقد فزت! نقاطك الآن: {points}.")
        
        won = "t.me/VIPABH/2"
        await event.reply(f"🎉 فزت! شاهد النتيجة هنا: {won}")
        
        game_active = False
    elif attempts >= max_attempts:
        await event.reply(f"للأسف، لقد نفدت محاولاتك. الرقم الصحيح هو {number}.")
        
        lose = "t.me/VIPABH/23"
        await client.send_voice(event.chat_id, lose)
        game_active = False
    else:
        await event.reply("جرب مرة أخرى، الرقم غلط💔")

if __name__ == "__main__":
    while True:
        try:
            # print("✨ بدء تشغيل العميل...")
            client.start()
            # print("✅ العميل يعمل الآن!")
            client.run_until_disconnected()
        except Exception as e:
            print(f"⚠️ حدث خطأ: {e}")
            print("⏳ إعادة المحاولة بعد 5 ثوانٍ...")
            time.sleep(5)


