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
            text = "یادگیری نامحدود تکنولوژی به صورت رایگان🧠 \n خوش اومدی به مموری لیک شو🙋🏻‍♂️ \n ویدیوهای آموزش برنامه نویسی و مباحث مرتبط هفتگی توی یوتوب آپلود میشه \n یادت نره سابسکرایب کنی👇\n https://www.youtube.com/@memoryleaksho?sub_confirmation=1",
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
