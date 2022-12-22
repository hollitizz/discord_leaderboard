from discord import Intents
from discord.ext import commands
import os

from utils.SQLRequests import SQLRequests


class UnknownUser(Exception):
    pass


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
        super().__init__("!", intents=Intents.all(), application_id=self.bot_id)
        self.db = SQLRequests()
        self.is_test_mode: bool = is_test_mode
        self.riot_token: str = os.getenv("RIOT_API_KEY")
