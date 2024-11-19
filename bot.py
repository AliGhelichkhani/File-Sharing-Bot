import sys
import requests
from aiohttp import web
from pyrogram import Client
from pyrogram.enums import ParseMode
from datetime import datetime
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT
from plugins import web_server

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def set_description(self):
        # Set the bot description via Telegram Bot API using an HTTP request
        description = "یادگیری نامحدود تکنولوژی به صورت رایگان🧠 \r\nخوش اومدی به مموری لیک شو🙋🏻‍♂️\r\nویدیوهای آموزش برنامه نویسی مباحث مرتبط هفتگی توی یوتوب آپلود میشه\r\nیادت نره سابسکرایب کنی👇🏻\r\nhttps://www.youtube.com/@memoryleaksho?sub_confirmation=1\r\nچنل تلگرام 👇🏻\r\n@MemoryLeakSho"  # Replace with your desired description
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/setMyDescription"
        params = {"description": description}

        try:
            response = requests.post(url, data=params)
            result = response.json()
            if result["ok"]:
                self.LOGGER(__name__).info("Bot description set successfully!")
            else:
                self.LOGGER(__name__).warning(f"Failed to set bot description: {result}")
        except Exception as e:
            self.LOGGER(__name__).warning(f"Failed to set bot description: {e}")

    async def start(self):
        # Call the set_description method before starting the bot
        await self.set_description()

        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(
                    f"Please double-check the FORCE_SUB_CHANNEL value and make sure the bot is an admin "
                    f"in the channel with Invite Users via Link permission. Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}"
                )
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Make sure the bot is an admin in the DB Channel, and double-check the CHANNEL_ID value. "
                f"Current Value: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running!\n\nCreated by https://t.me/CodeXBotz")
        print("Welcome to Memory Leak Sho File Sharing Bot")
        self.username = usr_bot_me.username

        # Start web server with aiohttp
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
