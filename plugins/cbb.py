#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = "📌 آدرس شبکه های اجتماعی:\r\n\r\nایمیل 📩 : \r\nmemoryleaksho@gmail.com\r\n\r\nاینستاگرام🔎:\r\nhttps://instagram.com/memoryleaksho\r\n\r\nیوتوب▶️:\r\nhttps://www.youtube.com/@memoryleaksho?sub_confirmation=1\r\n\r\nگیت‌هاب👾:\r\nhttps://github.com/MemoryLeakSho\r\n\r\nحمایت مالی🎁:\r\nhttps://zarinp.al/memoryleaksho\r\n\r\nپشتیبانی💬:\r\n@MemoryLeakShoContact \r\n\r\nگروه تلگرام 👥:\r\nt.me/MemoryLeakShoDiscussion\r\n\r\nگروه تخصصی🧑🏻‍💻:\r\nt.me/MemoryLeakShoTopics\r\n\r\nچت ناشناس👤:\r\nhttps://t.me/HidenChat_Bot?start=115463811\r\n\r\n\r\nمموری لیک شو | یادگیری نامحدود تکنولوژی به صورت رایگان. 🧠",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 بستن", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
