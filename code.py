from telethon import TelegramClient, events, Button
from models import add_or_update_user, add_point_to_winner, get_user_score
from bs4 import BeautifulSoup
import requests
import random
import time
from datetime import datetime
import os
#########
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('new_bot_session', api_id, api_hash).start(bot_token=bot_token)
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
    global number2
    username = event.sender.username or "unknown"    
    markup = [
        [Button.inline("ابدأ اللعبة", b"startGame")]
    ]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        buttons=markup
    )
    await client.send_file(
        event.chat_id,
        "https://t.me/VIPABH/1210",  
        caption=f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        parse_mode="Markdown"
    )
@client.on(events.CallbackQuery(func=lambda call: call.data == b"startGame"))
async def handle_start_game(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'game_active': False, 'active_player_id': None}
    
    if not group_game_status[chat_id]['game_active']:
        group_game_status[chat_id]['game_active'] = True
        group_game_status[chat_id]['active_player_id'] = user_id
        
        global number2
        number2 = random.randint(1, 6)
        group_game_status[chat_id]['number2'] = number2
        
        await event.message.edit(reply_markup=None)
        await event.answer(f"العبة بدأت! رقمك هو: {number2}")






client.run_until_disconnected()
