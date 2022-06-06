from typing import NewType, List
from discord import Intents
from discord.ext import commands
import os

from utils.DbHandler import DbHandler
from utils.leaderboard.refreshStats import getPlayerStats

class User():
    def __init__(self, tag, name, id):
        self.tag: str = tag
        self.name: str = name
        self.tier: int = 0
        self.rank: int = 1
        self.lp: int = 0
        self.id: str = id

    async def setStats(self, riot_token: str):
        data = await getPlayerStats(riot_token, self)
        self.tier = data['tier']
        self.rank = data['rank']
        self.lp = data['lp']


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
        super().__init__("!", intents=Intents.all(), application_id=self.bot_id)
        DbHandler.__init__(self, db_path)
        self.is_test_mode: bool = is_test_mode
        self.riot_token: str = os.getenv("RIOT_API_KEY")

userList = NewType("userList", List[User])
