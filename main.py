import traceback


import aiohttp
import discord
from discord.ext import commands, tasks
import os
import inspect


import cogs
from commands.leaderboard import refresh


from utils.DbHandler import DbHandler


from events.onReactionAdd import onReactionAdd
from events.onReactionRemove import onReactionRemove
from events.onMemberRemove import onMemberRemove
from events.onMemberAdd import onMemberAdd
from events.onMessage import onMessage
from events.onReady import onReady

import dotenv

dotenv.load_dotenv()


class Setup(commands.Bot, DbHandler):
    def __init__(self, is_test_mode=False):
        if is_test_mode:
            self.token: str = os.getenv("TEST_TOKEN")
            self.guild_id: int = os.getenv("GUILD_TEST_ID")
            db_path: str = "dbTest.json"
            self.bot_id: int = os.getenv("BOT_TEST_ID")
        else:
            self.bot_id: int = os.getenv("BOT_ID")
            self.token: str = os.getenv("TOKEN")
            self.guild_id: int = os.getenv("GUILD_ID")
            db_path: str = "db.json"
        super().__init__("!", intents=discord.Intents.all(), application_id=self.bot_id)
        DbHandler.__init__(self, db_path)
        self.is_test_mode: bool = is_test_mode
        self.riot_token: str = os.getenv("RIOT_API_KEY")

    async def setup_hook(self):
        self.session = aiohttp.ClientSession
        for cogName, _ in inspect.getmembers(cogs):
            if inspect.isclass(_):
                await self.load_extension(f"cogs.{cogName}")
            await bot.tree.sync(guild=discord.Object(id=self.guild_id))
        self.backgroundTask.start()

    @tasks.loop(minutes=5)
    async def backgroundTask(self):
        try:
            await refresh.loopedRefresh(self)
        except:
            traceback.print_exc()

    @backgroundTask.before_loop
    async def waitBackgroundTask(self):
        await self.wait_until_ready()

    async def on_reaction_add(self, reaction, user):
        await onReactionAdd(self, reaction, user)

    async def on_reaction_remove(self, reaction, user):
        await onReactionRemove(self, reaction, user)

    async def on_member_add(self, member):
        await onMemberAdd(self, member)

    async def on_member_remove(self, member):
        await onMemberRemove(self, member)

    async def on_message(self, message):
        await onMessage(self, message)

    async def on_ready(self):
        await onReady(self)


try:
    bot = Setup(is_test_mode=True)
    bot.run(bot.token, reconnect=True)
except KeyboardInterrupt:
    print("\nExiting...")
