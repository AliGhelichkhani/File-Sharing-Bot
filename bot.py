
from aiohttp import web
from plugins import web_server
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import requests
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT


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

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Set bot description and about text via HTTP API
        bot_token = TG_BOT_TOKEN
        api_url = f"https://api.telegram.org/bot{bot_token}"

        # Set the bot's description
        try:
            description_response = requests.post(
                f"{api_url}/setMyDescription",
                json={"description": "This bot allows you to share files effortlessly."}
            )
            description_response.raise_for_status()  # Raise an error for bad status codes
        except requests.exceptions.RequestException as e:
            self.LOGGER(__name__).warning(f"Failed to set bot description: {e}")

        # Set the bot's short description (about text)
        try:
            short_description_response = requests.post(
                f"{api_url}/setMyShortDescription",
                json={"short_description": "Memory Leak Sho File Sharing Bot"}
            )
            short_description_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.LOGGER(__name__).warning(f"Failed to set bot short description: {e}")

        # Original functionality for FORCE_SUB_CHANNEL
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

        # Original functionality for DB channel
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

        # Web server response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
