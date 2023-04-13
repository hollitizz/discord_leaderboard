from utils.SQLRequests import SQLRequests
from events import onReady, onMemberJoin, onMemberLeave, onGuildJoin, onGuildLeave
from commands.leaderboard import refresh
import cogs
import os
import inspect
import aiohttp
import discord
from discord.ext import commands, tasks
import logging


_logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, is_test_mode=False):
        if is_test_mode:
            self.token: str = os.getenv("TEST_TOKEN")
            self.guild_id: int = int(os.getenv("GUILD_TEST_ID"))
            self.bot_id: int = int(os.getenv("BOT_TEST_ID"))
        else:
            self.bot_id: int = int(os.getenv("BOT_ID"))
            self.token: str = os.getenv("TOKEN")
            self.guild_id: int = int(os.getenv("GUILD_ID"))
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(), application_id=self.bot_id
        )
        self.riot_token: str = os.getenv("RIOT_API_KEY")
        self.is_test_mode: bool = is_test_mode
        self.db = SQLRequests()

    async def setup_hook(self):
        self.session = aiohttp.ClientSession
        _logger.info("Loading commands...")
        for cogName, cog in inspect.getmembers(cogs):
            if inspect.isclass(cog):
                await self.load_extension(f"cogs.{cogName}")
        await self.tree.sync()
        _logger.info("Commands loaded")
        self.autoRefreshTask.start()

    @tasks.loop(minutes=10)
    async def autoRefreshTask(self):
        await refresh.loopedRefresh(self)

    @autoRefreshTask.before_loop
    async def waitAutoSaveTask(self):
        await self.wait_until_ready()

    async def on_ready(self):
        await onReady.onReady(self)

    async def on_member_join(self, member: discord.Member):
        await onMemberJoin.onMemberJoin(self, member)

    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        await onMemberLeave.onMemberLeave(self, payload)

    async def on_guild_join(self, guild: discord.Guild):
        await onGuildJoin.onGuildJoin(self, guild)

    async def on_guild_remove(self, guild: discord.Guild):
        await onGuildLeave.onGuildLeave(self, guild)

    async def on_command_error(self, ctx, error):
        _logger.error(error)