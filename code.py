from telethon import TelegramClient, events, Button
api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    global message, username
    builder = event.builder
    query = event.text

    if query.strip(): 
        parts = query.split(' ')
        if len(parts) >= 2: 
            message = ' '.join(parts[:-1]) 
            username = parts[-1] 
            
            if not username.startswith('@'):
                username = f'@{username}'
            
            try:
                whisper_id = f"{event.sender_id}:{username}"  # يمكن استخدام sender_id و username كـ id فريد للهمسة

                # تخزين الهمسة في قاعدة البيانات
                store_whisper(whisper_id, event.sender_id, username, message)

                # إنشاء الهمسة مع زر
                result = builder.article(
                    title='اضغط لارسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى \n الله يثخن اللبن عمي ({username})",
                    buttons=[Button.inline(text='tap to see', data=f'send:{username}:{message}:{event.sender_id}:{whisper_id}')]
                )
            except Exception as e:
                result = builder.article(
                    title='لرؤية المزيد حول الهمس',
                    description="همس",
                    text='اضغط هنا'
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
                if f"@{event.sender.username}" == username or str(event.sender_id) == sender_id:
                    await event.answer(f"{whisper.message}", alert=True)
                else:
                    await event.answer("هذه الرسالة ليست موجهة لك!", alert=True)
            else:
                await event.answer("لم يتم العثور على الهمسة!", alert=True)

        except Exception as e:
            await event.answer(f'حدث خطأ: {str(e)}', alert=True)
