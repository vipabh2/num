from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserNotParticipantError, ParticipantIdInvalidError
from telethon.tl.types import ChatBannedRights, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
import requests, os, operator, asyncio, random, uuid, datetime, re
from playwright.async_api import async_playwright # type: ignore
from database import store_whisper, get_whisper #type: ignore
from telethon.tl.types import KeyboardButtonCallback
from telethon import TelegramClient, events, Button
from db import save_date, get_saved_date #type: ignore
from hijri_converter import Gregorian
from telethon.tl.custom import Button
from googletrans import Translator
from bs4 import BeautifulSoup
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.NewMessage(pattern="ابن هاشم وين؟"))
async def t(event):
    await event.reply("انتتقل صديق المجموعة الاخ ابن هاشم الى حسابه الجديد **الخطير حسوني**")
    return
banned_words = [
    "ارقه جاي", "يموط", "تموط", "موطلي", "اموط", "بورن", "الفرخ", "الفرحْ", "تيز", "كسم"
    "مايا", "ماية", "مايه", "بكسمك", "بكسختك", "🍑", "نغل", "نغولة", "نغوله", "ينغل", 
    "سكسي", "كحاب", "مناويج", "منيوج", "عيورة", "عيورتكم", "انيجة", "انيچة", "انيجه", 
    "انيچه", "أناج", "اناج", "انيج", "أنيج", "فريخ", "فريخة", "فريخه", "فرخي","قضيب", 
    "🖕", "كسك", "كسه", "كسة", "اكحاب", "أكحاب", "زنا", "كوم بي", "كمبي", "ارقة جاي", 
    "اينيج", "بربوك", "زب", "طيزها", "عيري", "خرب الله", "العير", "بعيري", "كحبه", 
    "برابيك", "نيجني", "نيچني", "نودز", "نتلاوط", "لواط", "لوطي", "فروخ", "منيوك", 
    "انيجك", "نيجك", "كحبة", "ابن الكحبة", "ابن الكحبه", "تنيج", "اتنيج", "ينيج", 
    "كس", "عير", "كسمك", "كسختك", "كس امك", "طيز", "طيزك", "فرخ", "كواد", 
    
    ]
normalized_banned_words = {word: re.sub(r'(.)\1+', r'\1', word) for word in banned_words}
def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^أ-يa-zA-Z\s]', '', text)
    replace_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ؤ': 'و', 'ئ': 'ي'}
    for old, new in replace_map.items():
        text = text.replace(old, new)
    text = re.sub(r'(.)\1+', r'\1', text)
    return text
async def is_admin(chat, user_id):
    """التحقق مما إذا كان المستخدم مشرفًا أو منشئ المجموعة"""
    try:
        participant = await ABH(GetParticipantRequest(chat, user_id))
        return isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except:
        return False
def check_message(message):
    """التحقق مما إذا كانت الرسالة تحتوي على كلمة محظورة"""
    normalized_message = normalize_text(message)
    words = normalized_message.split()
    return any(word in normalized_banned_words.values() for word in words)
@ABH.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    if event.is_group:
        message_text = event.raw_text.strip()
        user_id = event.sender_id
        chat = await event.get_chat()
        if check_message(message_text):
            if await is_admin(chat, user_id):
                await event.delete()
                return
            me = await ABH.get_me()
            if not await is_admin(chat, me.id):
                return
            restrict_rights = ChatBannedRights(
                until_date=None,
                send_messages=True, 
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                embed_links=True
            )
            unrestrict_rights = ChatBannedRights(
                until_date=None,
                send_messages=False, 
                send_media=False,
                send_stickers=False,
                send_gifs=False,
                send_games=False,
                send_inline=False,
                embed_links=False
            )
            try:
                await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
                await event.delete()
                await asyncio.sleep(20 * 60)
                await ABH(EditBannedRequest(chat.id, user_id, unrestrict_rights))

            except Exception as e:
                return
questions_and_answers_s = [
    {"question": "أين أقيمت بطولة كأس العالم لكرة القدم عام 2002؟", "answer": ["كوريا الجنوبية واليابان", 'كوريا الجنوبية و اليابان']},
    {"question": "من هو اللاعب المعروف بأنه الهداف الأول في دوري أبطال أوروبا؟", "answer": ["كريستيانو رونالدو", 'رونالدو', "كرستيانو"]},
    {"question": "من اللاعب الحاصل على جائزة الكرة الذهبية في عام 2015م؟", "answer": ["كريستيانو رونالدو", 'رونالدو', "كرستيانو"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في أوروبا لعام 2020؟", "answer": ["روبرت ليفاندوفسكي", 'ليفاندوفسكي']},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في موسم واحد بالدوري الإنجليزي الممتاز؟", "answer": ["محمد صلاح"]},
    {"question": "ما هو النادي الذي حقق دوري أبطال أوروبا ثلاث مرات متتالية في الفترة الحديثة؟", "answer": ["ريال مدريد"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الإنجليزي الممتاز؟", "answer": ["مانشستر يونايتد"]},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في تاريخ الدوري الألماني؟", "answer": ["غيرد مولر"]},
    {"question": "من هو اللاعب الذي حصل على جائزة الحذاء الذهبي في كأس العالم 2014؟", "answer": ["رودريغيز"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في أفريقيا لعام 2019؟", "answer": ["ساديو ماني"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الإسباني؟", "answer": ["ريال مدريد"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الفرنسي؟", "answer": ["سانت إتيان"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في كأس العالم 2018؟", "answer": ["مودريتش"]},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في تاريخ كأس العالم؟", "answer": ["كلوزه"]},
    {"question": "ما هو أكبر ملعب لكرة القدم في العالم من حيث السعة؟", "answer": ["ملعب رونغرادو"]},
    {"question": "من هو المدرب الذي قاد منتخب ألمانيا للفوز بكأس العالم 2014؟", "answer": ["لوف"]},
    {"question": "ما هي الدولة التي فازت بأكبر عدد من بطولات كأس العالم؟", "answer": ["البرازيل"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'الشياطين الحمر'؟", "answer": ["مانشستر يونايتد"]},
    {"question": "ما هي الدولة التي فازت ببطولة كأس الأمم الأوروبية 2016؟", "answer": ["البرتغال"]},
    {"question": "من هو اللاعب الذي يُلقب بـ'البرغوث'؟", "answer": ["ليونيل ميسي", 'ميسي', "مسي"]},
    {"question": "متى سجل دييجو مارادونا هدفه الشهير باليد في كأس العالم؟", "answer": ["1986"]},
    {"question": "من هو اللاعب الذي سجل أسرع هدف في تاريخ كأس العالم؟", "answer": ["هاكان"]},
    {"question": "ما هي الدولة التي فازت بأول بطولة لكأس العالم؟", "answer": ["الاورغواي"]},
    {"question": "كم مرة فاز المنتخب السعودي بكأس آسيا لكرة القدم؟", "answer": ["3 مرات"]},
    {"question": "ما هو النادي الأكثر تحقيقًا للبطولات في العالم؟", "answer": ["ريال مدريد"]},
    {"question": "من هو النادي الأكثر مشاركة في الدوري الأوروبي؟", "answer": ["ريال مدريد"]},
    {"question": "ما هي الدولة التي فازت ببطولة كوبا أمريكا 2019؟", "answer": ["البرازيل"]},
    {"question": "من هو اللاعب الذي يُلقب بـ'الفتى الذهبي'؟", "answer": ["دييغو مارادونا"]},
    {"question": "ما هي الدولة التي ظهرت فيها كرة القدم لأول مرة؟", "answer": ["إنجلترا"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الملك' في كرة القدم؟", "answer": ["بيليه"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'المايسترو'؟", "answer": ["أندريا بيرلو"]},
    {"question": "ما هي الدولة التي استضافت كأس العالم 2006؟", "answer": ["ألمانيا"]},
    {"question": "ما هي الدولة التي استضافت كأس العالم 2010؟", "answer": ["افريقيا"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الماجيك'؟", "answer": ["رونالدينيو"]},
    {"question": "ما هي الدولة التي استضافت كأس العالم 1998؟", "answer": ["فرنسا"]},
    {"question": "متى أقيمت أول بطولة لكأس العالم لكرة القدم؟", "answer": ["1930"]},
    {"question": "ما هو تاريخ أول كأس عالم ومتى أقيم لأول مرة؟", "answer": ["1930"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الظاهرة'؟", "answer": ["رونالدو"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'العجوز'؟", "answer": ["يوفنتوس"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'الريدز'؟", "answer": ["ليفربول"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'البلوز'؟", "answer": ["تشيلسي"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'النسور'؟", "answer": ["لاتسيو"]},
    {"question": "في أي دولة أقيم كأس العالم الأول؟", "answer": ["الاورغواي"]},
    {"question": "المنتخب الاكثر فوز ب كأس العالم؟", "answer": ["البرازيل"]},
    {"question": "فريق كرة القدم يتكون من كم لاعب؟", "answer": ["11 لاعب"]},
    {"question": "من هو ال GOAT؟", "answer": ["رونالدو"]},
    {"question": "من هو عم برسا؟", "answer": ["رونالدو"]}
]
current_question = None
waiting_for_answer = False
@ABH.on(events.NewMessage(pattern='كرة قدم|/sport'))
async def start_s(event):
    global current_question, waiting_for_answer
    current_question = random.choice(questions_and_answers_s)
    waiting_for_answer = True
    await event.reply(f"{current_question['question']}")

@ABH.on(events.NewMessage)
async def check_answer_s(event):
    global current_question, waiting_for_answer
    user_message = event.text.strip().lower()

    if waiting_for_answer and current_question:
        correct_answer = [answer.lower() for answer in current_question.get('answer', [])]

        if user_message in correct_answer:
            await event.reply(f"إجابة صحيحة! ✅ {event.sender.first_name} جاوب صح 👏")
            current_question = None
            waiting_for_answer = False
        else:
            return
@ABH.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def permalink(event):
    global user, uid
    uid = event.sender_id
    user_id = event.pattern_match.group(1)
    if not user_id:
        await event.reply("استخدم الأمر كـ `كشف ايدي 1910015590`")
        return
    try:
        user = await event.client.get_entity(int(user_id))
    except Exception as e:
        return await event.reply(f"لا يوجد حساب بهذا الآيدي...")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    button = KeyboardButtonCallback("تغيير الئ رابط", b"recgange")
    await event.reply(f"⌔︙[{tag}](tg://user?id={user.id})", buttons=[button])
@ABH.on(events.CallbackQuery(data=b"recgange"))
async def chang(event):
    global user, uid
    sender_id = event.sender_id 
    if sender_id != uid:
        await event.answer("شلون وي الحشريين احنة \n عزيزي الامر خاص بالمرسل هوه يكدر يغير فقط😏", alert=True)
        return
    if uid is not None and sender_id == uid:
        await event.edit(f"⌔︙رابط المستخدم: tg://user?id={user.id}")
BANNED_SITES = [
    "porn", "xvideos", "xnxx", "redtube", "xhamster",
    "brazzers", "youjizz", "spankbang", "erotic", "sex"
]
DEVICES = {
    "pc": {"width": 1920, "height": 1080, "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    "android": "Galaxy S5"
}
def is_safe_url(url):
    return not any(banned in url.lower() for banned in BANNED_SITES)

async def take_screenshot(url, device="pc"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        if device in DEVICES:
            if isinstance(DEVICES[device], str):
                device_preset = p.devices[DEVICES[device]]
                context = await browser.new_context(**device_preset)
            else:
                context = await browser.new_context(
                    user_agent=DEVICES[device]["user_agent"],
                    viewport={"width": DEVICES[device]["width"], "height": DEVICES[device]["height"]}
                )
            page = await context.new_page()
        else:
            page = await browser.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            screenshot_path = f"screenshot_{device}.png"
            await page.screenshot(path=screenshot_path)
        except Exception as e:
            print(f"❌ خطأ أثناء تحميل الصفحة: {e}")
            screenshot_path = None
        finally:
            await browser.close()
    return screenshot_path
@ABH.on(events.NewMessage(pattern=r'كشف رابط|سكرين (.+)'))
async def handler(event):
    url = event.pattern_match.group(1)
    if not is_safe_url(url):
        await event.reply("هذا الموقع محظور! \nجرب تتواصل مع المطور @k_4x1")
        return
    devices = ['pc', 'android']
    screenshot_paths = []
    for device in devices:
        screenshot_path = await take_screenshot(url, device)
        if screenshot_path:
            screenshot_paths.append(screenshot_path)
    if screenshot_paths:
        await event.reply(f' تم التقاط لقطات الشاشة للأجهزة التالية: **PC، Android**:', file=screenshot_paths)
    else:
        await event.reply("🙄 هنالك خطأ أثناء التقاط لقطة الشاشة، تأكد من صحة الرابط أو جرب مجددًا.")
@ABH.on(events.NewMessage(pattern='^/dates$'))
async def show_dates(event):
    btton = [[
        Button.inline("محرم", b"m"),
        Button.inline("رمضان", b"rm"),
        Button.inline("شعبان", b"sh"),
        Button.inline("رجب", b"r"),
        Button.inline("حدد تاريخ", b"set_date")
    ]]
    await event.respond("اختر الشهر المناسب أو حدد تاريخ خاص 👇", buttons=btton)

@ABH.on(events.CallbackQuery)
async def handle_callback(event):
    data = event.data.decode("utf-8")
    if data == "set_date":
        await event.edit("من فضلك أدخل التاريخ بصيغة YYYY-MM-DD مثال: 2025-06-15", buttons=None)
    elif data == "m":
        await count_m(event)
    elif data == "rm":
        await count_rm(event)
    elif data == "sh":
        await count_sh(event)
    elif data == "r":
        await count_r(event)

@ABH.on(events.NewMessage(pattern=r'^\d{4}-\d{2}-\d{2}$'))
async def set_user_date(event):
    user_id = event.sender_id
    date = event.text
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        save_date(user_id, date)
        await event.reply(f"تم حفظ التاريخ {date}. يمكنك الآن معرفة كم باقي.")
    except ValueError:
        await event.reply("التاريخ المدخل غير صالح، يرجى إدخاله بصيغة YYYY-MM-DD.")

@ABH.on(events.NewMessage(pattern='^كم باقي$'))
async def check_remaining_days(event):
    user_id = event.sender_id
    saved_date = get_saved_date(user_id)
    if saved_date:
        t = datetime.datetime.today()
        saved_date_obj = datetime.datetime.strptime(saved_date, "%Y-%m-%d").date()
        days_difference = (saved_date_obj - t.date()).days
        msg = f"باقي {days_difference} ايام" if days_difference >= 0 else f"التاريخ قد مضى منذ {abs(days_difference)} يوم"
        await event.reply(msg)
    else:
        await event.reply("لم تحدد تاريخًا بعد، يرجى تحديد تاريخ أولاً.")

async def count_r(event):
    await calculate_days(event, datetime.date(2025, 12, 22))

async def count_sh(event):
    await calculate_days(event, datetime.date(2026, 1, 20))

async def count_rm(event):
    await calculate_days(event, datetime.date(2025, 3, 1))

async def count_m(event):
    await calculate_days(event, datetime.date(2025, 6, 26))

async def calculate_days(event, target_date):
    t = datetime.datetime.today()
    days_difference = (target_date - t.date()).days
    msg = f"باقي {days_difference} ايام" if days_difference >= 0 else "الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1"
    await event.edit(msg)

@ABH.on(events.NewMessage(pattern='^تاريخ$'))
async def start_handler(event):
    t = datetime.datetime.now().date()
    hd = Gregorian(t.year, t.month, t.day).to_hijri()
    hd_str = f"{hd.day} {hd.month_name('ar')} {hd.year} هـ"    
    await event.reply(f" الهجري: \n {hd_str} \n الميلادي: \n {t}")
c = [
    "ههههههه",
    "😂",
    "يسعدلي مسائك😀"
]
@ABH.on(events.NewMessage(pattern='ميم|ميمز'))
async def start(event):
    global c
    rl = random.randint(2, 273)
    url = f"https://t.me/IUABH/{rl}"
    cap = random.choice(c)
    await ABH.send_file(event.chat_id, url, caption=f"{cap}", reply_to=event.id)

@ABH.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text
    sender = event.sender_id
    if query.strip():
        parts = query.split(' ')
        if len(parts) >= 2:
            message = ' '.join(parts[:-1])
            recipient = parts[-1]
            try:
                if recipient.isdigit():
                    reciver_id = int(recipient)
                    username = f'ID:{reciver_id}'
                else:
                    if not recipient.startswith('@'):
                        recipient = f'@{recipient}'
                    reciver = await ABH.get_entity(recipient)
                    reciver_id = reciver.id
                    username = recipient
                whisper_id = str(uuid.uuid4())
                store_whisper(whisper_id, sender, reciver_id, username, message)
                result = builder.article(
                    title='اضغط لإرسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى \n الله يثخن اللبن عمي 😌 ({username})",
                    buttons=[
                        Button.inline(
                            text='🫵🏾 اضغط لعرض الهمسة',
                            data=f'send:{whisper_id}'
                        )
                    ]
                )
            except Exception as e:
                result = builder.article(
                    title='خطأ في الإرسال',
                    description="حدث خطأ أثناء معالجة طلبك.",
                    # text=f' خطأ: {str(e)}'
                )
        else:
            return
        await event.answer([result])
@ABH.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        whisper_id = data.split(':')[1]
        whisper = get_whisper(whisper_id)
        if whisper:
            if event.sender_id == whisper.sender_id or event.sender_id == whisper.reciver_id:
                await event.answer(f"{whisper.message}", alert=True)
            else:
                await event.answer("عزيزي الحشري، هذه الهمسة ليست موجهة إليك!", alert=True)
questions_and_answers = [
    {"question": "من هم ال البيت؟", "answer": ["هم اهل بيت رسول الله", 'اهل بيت رسول الله', "ال بيت رسول الله"]},
    {"question": "من هو الخليفة الاول؟", "answer": ["ابا الحسن علي", "الامام علي", "علي ابن ابي طالب"]},
    {"question": "كم عدد المعصومين؟", "answer": ["14", "اربع عشر"]},
    {"question": "كم عدد اهل البيت؟", "answer": ["12", "اثنا عشر"]},
    {"question": "ال**** هو نقل الكلام من ثقات الحديث", "answer": [ "التواتر", "تواتر"]},
    {"question": "من هو الدنيئ الذي غدر الامام علي بالمسجد يوم 19 رمضان؟", "answer": ["اللعين ابن ملجم", "ابن ملجم", "عبد الرحمن", "عبد الرحمن ابن ملجم"]},
    {"question": "من الذي قال يا ابن راعية المعزة وعلئ من؟", "answer": "الامام الحسين الشمر اللعين"},
    {"question": "الامام الذي بعد الامام علي؟", "answer": ["الحسن المجتبى", "الحسن", "الامام الحسن"]},
    {"question": "الامام الذي بعد الامام الحسن؟", "answer": ["الحسين الشهيد", "الامام الحسين"]},
    {"question": "بحق من نزلت اية التطهير؟", "answer": ["ال بيت رسول الله", "اهل البيت"]},
    {"question": "من هو سيف الله المسلول؟", "answer": ["الامير علي", "الامام علي"]},
    {"question": "من هو سيف الشيطان المذلول؟", "answer": "خالد"},
    {"question": "من هم الثقلين؟", "answer": ["كتاب الله واهل البيت", "كتاب الله و اهل البيت", "كتاب الله و اهل البيت"]},
    {"question": "من هو قمر عشيرة الهواشم؟", "answer": "الامام العباس"},
    {"question": "من هو كفيل زينب؟", "answer": "الامام العباس"},
    {"question": "من الذي قتل المحسن ابن علي؟", "answer": ["اللعين عمر", "عمر"]},
    {"question": "من هو قطيع الكفين؟", "answer": "الامام العباس"},
    {"question": "من هو شاعر قصيدة الله يا حامي الشريعة؟", "answer": "حيدر الحلي"},
    {"question": "من هو حامي الجار؟", "answer": "الامام علي"},
    {"question": "من صاحب قول \n أَمْلَأَ رُكابِي فِضَّةً أَوْ ذَهَبًا إِنِّي قَتَلْتُ خَيْرَ الرِّجَالِ أَمَّا وَأَبَا؟", "answer": "سنان بن انس"},
    {"question": "من هو سلمان المحمدي؟", "answer": "صحابي النبي و شهيد كربلاء"},
    {"question": "من هو الذي دفن مع الامام الحسين؟", "answer": "عبد الله الرضيع"},
    {"question": "ما هي اسم الواقعه في يوم العاشر من محرم؟", "answer": "واقعة الطف"},
    {"question": "ما هو اسم اليوم الذي استشهد فيه الامام الحسين؟", "answer": "عاشوراء"},
    {"question": "من هو الحجة المنتظر؟", "answer": "الامام المهدي"},
    {"question": "كم عدد المعصومين الذي اسمهم محمد؟", "answer": "2"},
    {"question": "ما هو اسم الامام المهدي؟", "answer": "محمد ابن الحسن"},
    {"question": "ما هي بيعة الغدير؟", "answer": ["تتويج الامام علي", "بيعة الامام علي"]},
    {"question": "من هو الذي تصدق في المحبس في الصلاة؟", "answer": "الامام علي"},
    {"question": "ما هو اسم المكان الذي تم تتويج الامام علي خليفة؟", "answer": "غدير خم"},
    {"question": "اين دفنت ام البنين؟", "answer": ["في البقيع", "في قبور البقيع"]},
    {"question": "متى ولادة الامام المهدي \n عجل الله فرجة الشريف؟", "answer": [" 15 من شعبان", "15 شعبان", "نصف شعبان"]},
    {"question": "من القائل , بين الحق والباطل 4 اصابع؟", "answer": "الامام علي"},
    {"question": "من هو الصادق الامين؟", "answer": "النبي محمد"},
    {"question": "من هو الرسول الاعظم؟", "answer": ["الرسول محمد" , "النبي محمد"]},
    {"question": "من هو قائد الغر المحجلين؟", "answer": "الامام علي"},
    {"question": "من قائل مثلي لا يبايع مثله؟", "answer": "الامام الحسين"},
    {"question": "الان انكسر ظهري \n قالها الحسين لكن بحق من؟", "answer": "الامام العباس"},
    {"question": "من هو الفاروق الاعظم؟", "answer": "الامام علي"},
    {"question": "من هو سيد الشهداء؟", "answer": "الامام الحسين"},
    {"question": "من هو الذي اسقط عائشة في حرب الجمل؟", "answer": "الامام الحسن"},
    {"question": "ما انصفوكِ صانوا حرائرهم واخرجوكِ \n قالها الامام علي لكن بحق من؟", "answer": "عائشة"},
    {"question": "الخسف في البيداء هي علامة من علامات؟", "answer": "ظهور الامام"},
    {"question": "من هو عليل كربلاء؟", "answer": ["الامام السجاد", "الامام زين العابدين"]},
    {"question": "من الاعظم النبوة ام الامامة؟", "answer": "الامامة"},
    {"question": "من هو عميد المنبر الحسيني؟", "answer": "احمد الوائلي"},
    {"question": "من هو زعيم الحوزه العلمية؟", "answer": ["ابو القاسم الخوئي", "الخوئي"]},
    {"question": "ما هو حكم التطبير حسب قول العلماء؟", "answer": "حلال"},
    {"question": "ما هو حكم سماع الاغاني؟", "answer": "حرام"},
    {"question": "ما هو حكم التدخين؟", "answer": "حلال"},
    {"question": "من هو عون؟", "answer": "ابن السيدة زينب"},
    {"question": "من المنتصر في حرب الجمل؟", "answer": "الامام علي"},
    {"question": "كم عدد الخوارج في واقعةالطف؟", "answer": ["70 الف", "سبعين الف", "سبعون الف"]},
    {"question": "من هو مفرح قلب الزهراء؟", "answer": "ابو لؤلؤة"}
]
current_question = None
waiting_for_answer = False
@ABH.on(events.NewMessage(pattern='اسئلة|/quist'))
async def start_1(event):
    global current_question, waiting_for_answer
    current_question = random.choice(questions_and_answers)
    waiting_for_answer = True
    await event.reply(f"{current_question['question']}")

@ABH.on(events.NewMessage)
async def check_answer_s(event):
    global current_question, waiting_for_answer
    user_message = event.text.strip().lower()

    if waiting_for_answer and current_question:
        correct_answer = [answer.lower() for answer in current_question.get('answer', [])]

        if user_message in correct_answer:
            await event.reply(f"إجابة صحيح احسنت")
            current_question = None
            waiting_for_answer = False
        else:
            return         
player1 = None
player2 = None
turn = None  
game_board = [" " for _ in range(9)] 
restart_confirmations = {}
@ABH.on(events.NewMessage(pattern='اكس او|/xo|/Xo'))
async def start_message(event):
    global player1, player2, username1, t1
    player1 = event.sender_id
    username1 = event.sender.username or "unknown"
    t1 = event.sender.first_name or "unknown"
    markup = [[Button.inline("ابدأ اللعبة", b"start")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username1})! تم تسجيلك في لعبة x o انت الاعب الاول و دورك هو x.",
        file="https://t.me/VIPABH/1216",  
        parse_mode="Markdown",
        buttons=markup
    )
@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"start"))
async def start_game(event):
    global player1, player2, turn, game_board, username1, username2, t1, t2
    player2 = event.sender_id
    username2 = event.sender.username or "unknown"
    t2 = event.sender.first_name or "unknown"
    if player1 == player2:
        await event.answer(" لا يمكنك اللعب ضد نفسك يا متوحد!")
        return
    if player2 == 7017022402:
        return
    turn = player1
    game_board = [" " for _ in range(9)]
    await show_board(event)
async def show_board(event, winner=None):
    if winner:
        markup = [
            [Button.inline("إعادة اللعبة", b"restart"), Button.inline("إلغاء", b"cancel")]
        ]
        await event.edit(
            f"اللاعب [{winner['name']}](https://t.me/{winner['username']}) فاز باللعبة!",
            buttons=markup,
            parse_mode="Markdown"
        )
    elif " " not in game_board:
        markup = [
            [Button.inline("إعادة اللعبة", b"restart"), Button.inline("إلغاء", b"cancel")]
        ]
        await event.edit(
            "اللعبة انتهت بالتعادل!",
            buttons=markup,
            parse_mode="Markdown"
        )
    else:
        markup = [
            [Button.inline(game_board[0], b"move_0"), Button.inline(game_board[1], b"move_1"), Button.inline(game_board[2], b"move_2")],
            [Button.inline(game_board[3], b"move_3"), Button.inline(game_board[4], b"move_4"), Button.inline(game_board[5], b"move_5")],
            [Button.inline(game_board[6], b"move_6"), Button.inline(game_board[7], b"move_7"), Button.inline(game_board[8], b"move_8")]
        ]
        
        current_player = t1 if turn == player1 else t2
        current_username = username1 if turn == player1 else username2
        try:
            await event.edit(
                f"اللاعب الأول —> [{t1}](https://t.me/{username1})\nاللاعب الثاني —> [{t2}](https://t.me/{username2})\n\nدور اللاعب —> [{current_player}](https://t.me/{current_username})",
                buttons=markup,
                parse_mode="Markdown")
              
        except Exception:
            await event.reply(
                f"اللاعب الأول —> [{t1}](https://t.me/{username1})\nاللاعب الثاني —> [{t2}](https://t.me/{username2})\n\nدور اللاعب —> [{current_player}](https://t.me/{current_username})",
                buttons=markup,
                parse_mode="Markdown"
            )
@ABH.on(events.CallbackQuery(func=lambda call: call.data.startswith(b"move_")))
async def make_move(event):
    global game_board, turn, t1, t2
    move = int(event.data.decode("utf-8").split("_")[1])
    
    if move < 0 or move >= len(game_board):
        await event.answer("التحرك غير صالح! اختر مربعاً آخر.")
        return
    if game_board[move] != " ":
        await event.answer("المربع هذا مشغول بالفعل! اختر مربعاً آخر.")
        return
    if event.sender_id == player1 and turn == player1:
        game_board[move] = "X"
        turn = player2  
    elif event.sender_id == player2 and turn == player2:
        game_board[move] = "O"
        turn = player1 
    else:
        await event.answer("ليس دورك الآن!")
        return
    winner = check_winner()
    if winner:
        winner_name = t1 if winner == "X" else t2
        winner_username = username1 if winner == "X" else username2
        await show_board(event, winner={"name": winner_name, "username": winner_username})
    elif " " not in game_board:
        await show_board(event)
    else:
        await show_board(event)
def check_winner():
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for line in lines:
        if game_board[line[0]] == game_board[line[1]] == game_board[line[2]] and game_board[line[0]] != " ":
            return game_board[line[0]]  
    return None
@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"restart"))
async def restart_game(event):
    global restart_confirmations, player1, player2, turn, game_board
    player_id = event.sender_id
    restart_confirmations[player_id] = True
    if player1 in restart_confirmations and player2 in restart_confirmations:
        game_board = [" " for _ in range(9)]
        turn = player1
        restart_confirmations = {}
        await show_board(event)
    else:
        await event.answer("في انتظار موافقة اللاعب الآخر لإعادة اللعبة.")
@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"cancel"))
async def cancel_game(event):
    await event.edit("تم إلغاء اللعبة.")
def reset_game():
    global game_board, player1, player2, turn
    game_board = [" " for _ in range(9)]  
    player1 = None
    player2 = None
    turn = None
if not any([player1, player2]): 
    reset_game()    
@ABH.on(events.NewMessage(pattern=r'\bاحس\b'))
async def mem1(event):
        url = "https://files.catbox.moe/euqqqk.jpg"  
        await event.client.send_file(event.chat_id, url, reply_to=event.message.id)
operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}
@ABH.on(events.NewMessage(pattern=r'احسب (\d+)\s*([\+\-\*/÷])\s*(\d+)'))
async def calc(event):
    try:
        match = event.pattern_match 
        a = int(match.group(1))
        mark = match.group(2)
        b = int(match.group(3))
        if mark in operations:
            result = operations[mark](a, b)
            await event.respond(f"النتيجة `{result}`", reply_to=event.message.id)
        else:
            await event.respond("عملية غير مدعومة!", reply_to=event.message.id)
    except ZeroDivisionError:
        await event.respond("خطأ: لا يمكن القسمة على صفر!", reply_to=event.message.id)
abh = [
    "ها",
    "تفظل",
    "كول",
    "اسمعك",
    "شرايد",
    "خلصني",
    "https://t.me/VIPABH/1214",
    "https://t.me/VIPABH/1215"
]
@ABH.on(events.NewMessage(pattern=r'^مخفي$'))
async def reply(event):
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await event.reply(file=vipabh)
    else:
        await event.reply(vipabh)
translator = Translator()
@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def handle_message(event):
    if event.is_reply:
        replied_message = await event.get_reply_message()
        original_text = replied_message.text
    else:
        command_parts = event.message.text.split(' ', 1)
        original_text = command_parts[1] if len(command_parts) > 1 else None
    if not original_text:
        await event.reply("عزيزي ...\n يرجئ كتابة النص مع الامر او بالرد عليه.")
        return
    detected_language = translator.detect(original_text).lang
    if detected_language == "ar":
        translated = translator.translate(original_text, dest="en")
    else:
        translated = translator.translate(original_text, dest="ar")
    response = (
        f" **اللغة المكتشفة:** `{detected_language}`\n"
        f" **النص المترجم:** `{translated.text}`"
        )
    await event.reply(response)
@ABH.on(events.NewMessage(pattern='ابن هاشم'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        rl = random.randint(1222, 1241)
        url = f"https://t.me/VIPABH/{rl}"
        caption = "أبن هاشم (رض) مرات متواضع ،🌚 @K_4x1"
        button = [Button.url(text="الking", url="https://t.me/K_4x1")]
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id, buttons=button)
    else:
        return
@ABH.on(events.NewMessage(pattern='زهراء'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        url = "https://t.me/VIPABH/1220"  
        caption = "@klix_78 ( لَقَدْ كَفَرَ الّذِينَ قَالُوا إنَّ الله هُو المَسِيحُ ابْنُ مَرْيَم)." 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='امريجا|الامريكي'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        url = "https://files.catbox.moe/p9e75j.mp4"  
        caption = "@l_h_2" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='امير'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        ur = ["https://files.catbox.moe/k44qq6.mp4",
               'https://t.me/KQK4Q/23',
               'https://t.me/KQK4Q/22'
               ]
        url = random.choice(ur)
        caption = "@xcxx1x" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='عبدالله|عبود'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        url = "https://files.catbox.moe/qohqtp.MP4"  
        caption = "@UU77QQ" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
auto = [
        "ع س",
        "عليكم السلام",
        "عليكم السلام والرحمة والاكرام",
        "عليكم سلام الله"
        ]
@ABH.on(events.NewMessage(pattern=r'^(سلام عليكم|السلام عليكم)$'))
async def reply_abh(event):
        abh = random.choice(auto)
        await event.reply(abh)    
@ABH.on(events.NewMessage(pattern=r'^(مخفي طكة زيج|زيج)$'))
async def reply_abh(event):
    replied_message = await event.get_reply_message()
    if replied_message and replied_message.sender_id == 1910015590:
        await event.reply("عزيزي الغبي ... \n تريدني اعفط للمطور شكلت لربك؟")
        return
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/VIPABH/1171", reply_to=replied_message.id)
    else:
        await event.reply("عزيزي الفاهي ... \n الامر يعمل بالرد , اذا عدتها وما سويت رد اعفطلك")
@ABH.on(events.NewMessage(pattern=r'^(ميعرف|مايعرف)$'))
async def reply_abh(event):
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/3", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/3", reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r'^(صباح النور|صباح الخير)$'))
async def reply_abh(event):
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/4", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/4", reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r'^(لا تتمادة|لا تتماده|تتماده)$'))
async def reply_abh(event):
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/5", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/5", reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r'^(هاي بعد|اي هاي)$'))
async def reply_abh(event):
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/6", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/6", reply_to=event.message.id)
url = "https://ar.wikipedia.org/w/api.php"
searching_state = {}
@ABH.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower().startswith('ابحث عن')))
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
        await event.answer([result])

searching_state = {}
@ABH.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower().startswith('ابحث عام')))
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
@ABH.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower() in ['عاشوراء']))
async def ashouau(event):
    pic = "links/abh.jpg"
    await ABH.send_file(event.chat_id, pic, caption="تقبل الله صالح الأعمال", reply_to=event.message.id)
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
@ABH.on(events.NewMessage(pattern='/rings'))
async def start_game(event):
    username = event.sender.username or "unknown"
    markup = [[Button.inline("ابدأ اللعبة", b"startGame")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        file="https://t.me/VIPABH/1210",  
        parse_mode="Markdown",
        buttons=markup
    )
    
@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"startGame"))
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
@ABH.on(events.NewMessage(pattern=r'جيب (\d+)'))
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
                await event.reply("❗ يرجى إدخال رقم صحيح بين 1 و 6.")
        except (IndexError, ValueError):
            await event.reply("❗ يرجى إدخال رقم صحيح بين 1 و 6.")
        
@ABH.on(events.NewMessage(pattern=r'طك (\d+)'))
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
            
@ABH.on(events.NewMessage(pattern='/محيبس'))
async def show_number(event):
    """إظهار الرقم السري عند الطلب وإرساله إلى @k_4x1"""
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        target_user_id = 1910015590  
        await ABH.send_message(target_user_id, f"الرقم السري هو: {number2}")
        await event.reply("تم إرسال الرقم السري إلى @k_4x1.")
    else:
        await event.reply("لم تبدأ اللعبة بعد. أرسل /rings لبدء اللعبة.")
mohmurl = random.randint(119, 138)
basimurl = random.randint(50, 118)
musurl = random.randint(139, 154)
nurl = random.randint(164, 170)
furl = random.randint(171, 174)

async def send_audio_from_list(event, url_list):
    rl = random.choice(url_list)
    audio_url = f"https://t.me/sossosic/{rl}"
    await event.reply(file=audio_url)

banned_url = [
    9,  25, 94, 131, 175,
    26, 40, 110, 136, 194,
    71, 72, 111, 142, 212,
    77, 79, 114, 148,
    80, 81, 115, 150,
    82, 93, 121, 152
]

latmiyat_range = range(50, 257)

async def send_random_latmia(event):
    try:
        chosen = random.choice(list(latmiyat_range))
        if chosen in banned_url:
            return await send_random_latmia(event)
        latmia_url = f"https://t.me/x04ou/{chosen}"
        await event.reply(file=latmia_url)
    except Exception as e:
        await event.reply(f"حدث خطأ أثناء الإرسال: {str(e)}")

@ABH.on(events.NewMessage(pattern=r"^(لطمية|لطميه)$"))
async def handle_latmia_command(event):
    await send_random_latmia(event)

@ABH.on(events.NewMessage(pattern='^/start$'))
async def handle_start(event):
    await event.reply(
        "أهلاً حياك الله! \n\n"
        "• أرسل /xo ل بدء لعبة xo \n"
        "• أرسل `لطمية` ل ارسال لطمية\n"
        "• أرسل /num لبدء لعبة الأرقام.\n"
        "• أرسل `ميم` او `ميمز` للميمز. \n"
        "• أرسل `كتويت` لبدء أسئلة الكتتويت.\n"
        "• أرسل /quist او `اسئلة`اسئلة دينية. \n"
        "• أرسل `ابحث عن` لعمل بحث في ويكيبيديا \n"
        "• أرسل /rings لبدء لعبة محيبس الكتتويت. \n"
        "• أرسل `النقاط` ل رؤية نقاطك في لعبة /num \n"
        "• الامر او بالرد `ترجمة` لترجمه نص مع لطمية\n"
        "• أرسل `احسب` لحساب معادلة بالرد او مع الامر\n"
        "• أرسل `ابحث عام` يعمل بحث لكن ليس دقيق ب 3 نتائج \n\n"
        "استمتع! 🎉",
        parse_mode='markdown'
        )
        
def add_or_update_user(user_id):
    if user_id not in user_points:
        user_points[user_id] = 0  
            
def add_point_to_winner(user_id):
    if user_id in user_points:
        user_points[user_id] += 1 

def get_user_score(user_id):
    return user_points.get(user_id, 0)
user_points = {}
game_active = False
number = None
max_attempts = 3
attempts = 0
active_player_id = None
@ABH.on(events.NewMessage(pattern='/num'))
async def start_game(event):
    global game_active, number, attempts, active_player_id
    if game_active:
        await event.reply("اللعبة قيد التشغيل بالفعل! حاول إنهاء اللعبة الحالية أولاً.")
        return
    username = event.sender.username if event.sender.username else "لا يوجد اسم مستخدم"
    markup = [[Button.inline("ابدأ اللعبة", b"start_game")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        file="https://t.me/VIPABH/1204",
        parse_mode="Markdown",
        buttons=markup
    )
@ABH.on(events.CallbackQuery(data=b"start_game"))
async def initiate_game(event):
    global game_active, number, attempts, active_player_id
    game_active = True
    number = random.randint(1, 10)
    attempts = 0
    active_player_id = event.sender_id
    await event.answer("🎮 اللعبة بدأت!")
    await event.edit("🎲 اللعبة بدأت! حاول تخمين الرقم (من 1 إلى 10).")
@ABH.on(events.NewMessage(func=lambda event: game_active and event.sender_id == active_player_id))
async def handle_guess(event):
    global game_active, number, attempts, max_attempts
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
        add_or_update_user(event.sender_id)
        add_point_to_winner(event.sender_id)
        points = get_user_score(event.sender_id)
        msg1 = await event.reply("🥳")
        await asyncio.sleep(3)
        await msg1.edit("🎉مُبارك! لقد فزت!")
        game_active = False
    elif attempts >= max_attempts:
        await event.reply(f"للأسف، لقد نفدت محاولاتك. الرقم الصحيح هو {number}.")
        lose = "https://t.me/VIPABH/23"
        await ABH.send_message(event.chat_id, file=lose)
        game_active = False
    else:
        await event.reply("جرب مرة أخرى، الرقم غلط💔")
@ABH.on(events.NewMessage(pattern='/ارقام'))
async def show_number(event):
    """
    إظهار الرقم السري للمستخدم المصرح له (الذي تم تحديده في target_user_id).
    """
    global game_active, number
    chat_id = event.chat_id
    target_user_id = 1910015590 
    if game_active:
        # try:
            ms1 = await ABH.send_message(target_user_id, f"🔒 الرقم السري هو: {number}")
            await event.reply("تم إرسال الرقم السري إلى @k_4x1.")
            await asyncio.sleep(10)
            await ABH.delete_messages(ms1.chat_id, [ms1.id])  
        # except Exception as e:
        #     await event.reply(f"حدث خطأ: {str(e)}")
    else:
        await event.reply("⚠️ لم تبدأ اللعبة بعد. أرسل /num لبدء اللعبة.")
@ABH.on(events.NewMessage(pattern='النقاط')) 
async def show_points(event):
    user_id = event.sender_id  
    points = get_user_score(user_id) 
    await event.reply(f"📊 نقاطك الحالية هي: {points} 🌟")
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
@ABH.on(events.NewMessage(func=lambda event: event.text in ['كتويت']))
async def send_random_question(event):
    random_question = random.choice(questions)
    await event.reply(random_question)
ABH.run_until_disconnected()
