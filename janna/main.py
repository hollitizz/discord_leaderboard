import aiohttp
import discord
from discord.ext import commands, tasks
import os
import inspect

import cogs
from commands.leaderboard import refresh


from events.onReady import onReady


import dotenv
import logging

from utils.SQLRequests import SQLRequests

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
                logging.info(f"{cogName} commands loaded!")
        await bot.tree.sync(guild=discord.Object(id=self.guild_id))
        if self.is_test_mode:
            logging.info("Test mode: Background tasks disabled")
            return
        self.autoRefreshTask.start()

    @tasks.loop(minutes=5)
    async def autoRefreshTask(self):
        await refresh.loopedRefresh(self)

    @autoRefreshTask.before_loop
    async def waitAutoSaveTask(self):
        await self.wait_until_ready()

    async def on_ready(self):
        await onReady(self)

    async def on_command_error(self, ctx, error):
        logging.error(error)

try:
    bot = Setup(is_test_mode=False)
    bot.run(bot.token, reconnect=True, log_handler=None)
except KeyboardInterrupt:
    logging.warning("\nExiting...")
