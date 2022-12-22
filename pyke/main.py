import aiohttp
import discord
from discord.ext import commands, tasks
import os
import inspect

import cogs


from events.onScheduledEventCreate import onScheduledEventCreate
from events.onMemberRemove import onMemberRemove
from events.onMemberJoin import onMemberJoin
from events.onReady import onReady


import dotenv
import logging

from utils.SQLRequests import SQLRequests
from utils.exportDatabase import exportDataBase
from utils.cleanSaveFolder import cleanSaveFolder

dotenv.load_dotenv()
discord.utils.setup_logging()


class Setup(commands.Bot):
    def __init__(self, is_test_mode=False):
        if is_test_mode:
            self.token: str = os.getenv("TEST_TOKEN")
            self.guild_id: int = int(os.getenv("GUILD_TEST_ID"))
            self.bot_id: int = int(os.getenv("BOT_TEST_ID"))
        else:
            self.bot_id: int = int(os.getenv("BOT_ID"))
            self.token: str = os.getenv("TOKEN")
            self.guild_id: int = int(os.getenv("GUILD_ID"))
        super().__init__("!", intents=discord.Intents.all(), application_id=self.bot_id)
        self.db = SQLRequests()
        self.is_test_mode: bool = is_test_mode
        self.riot_token: str = os.getenv("RIOT_API_KEY")

    async def setup_hook(self):
        self.session = aiohttp.ClientSession
        for cogName, _ in inspect.getmembers(cogs):
            if inspect.isclass(_):
                logging.info(f"Loading {cogName} commands...")
                await self.load_extension(f"cogs.{cogName}")
                await self.tree.sync(guild=discord.Object(id=self.guild_id))
                logging.info(f"{cogName} commands loaded!")
        if self.is_test_mode:
            logging.info("Test mode: Background tasks disabled")
            return
        if os.path.isdir(os.getenv("DB_SAVE_PATH")) and self.db is not None:
            self.exportDataBaseTask.start()
        else:
            logging.warning(f"DB_SAVE_PATH is not a valid directory, auto save task is disabled")

    @tasks.loop(hours=24)
    async def exportDataBaseTask(self):
        exportDataBase()
        cleanSaveFolder()

    @exportDataBaseTask.before_loop
    async def before_exportDataBaseTask(self):
        await self.wait_until_ready()

    async def on_member_join(self, member):
        await onMemberJoin(self, member)

    async def on_member_remove(self, member):
        await onMemberRemove(self, member)

    async def on_scheduled_event_create(self, event):
        await onScheduledEventCreate(self, event)

    async def on_ready(self):
        await onReady(self)

    async def on_command_error(self, ctx, error):
        logging.error(error)

try:
    bot = Setup(is_test_mode=True)
    bot.run(bot.token, reconnect=True, log_handler=None)
except KeyboardInterrupt:
    logging.warning("\nExiting...")
