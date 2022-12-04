from typing import NewType, List
from discord import Intents
from discord.ext import commands
import os

from utils.DbHandler import DbHandler
from utils.leaderboard.getPlayerStats import getPlayerStats


class UnknownUser(Exception):
    pass

WELCOME_MESSAGE ="""
--------------------------------------------------------------------------------------------------------------

☆ Pour bien commencer (et après avoir accepté les règles), tu peux :

✦ Tu peux envoyer le lien de ton opgg (https://euw.op.gg/) dans le channel <#832306284593152050> si tu le souhaites !

✦ Tu peux également te présenter dans <#834846943858786384>

✦ Tu cherches un ou plusieurs mates ? Le channel <#834882281360457738> est fait pour toi !

✦ Si tu as besoin d'aide pour t'améliorer dans le jeu n'hésite pas à en faire la demande !

✦ Des events sont régulièrement organisés alors garde toujours un œil sur le channel <#834835968791150612> ! :SorakaLove:

--------------------------------------------------------------------------------------------------------------

https://discord.gg/t4RbZfM7aY
"""

class User():
    def __init__(self, tag, name, id):
        self.tag: str = tag
        self.name: str = name
        self.tier: int = 0
        self.rank: int = 1
        self.lp: int = 0
        self.id: str = id
        self.is_displayed: bool = True

    async def setStats(self, riot_token: str):
        try:
            fetch_user = await getPlayerStats(riot_token, User(self.tag, self.name, self.id))
            self.tier = fetch_user.tier
            self.rank = fetch_user.rank
            self.lp = fetch_user.lp
        except:
            pass


class Setup(commands.Bot, DbHandler):
    def __init__(self, is_test_mode=False):
        if is_test_mode:
            self.token: str = os.getenv("TEST_TOKEN")
            self.guild_id: int = int(os.getenv("GUILD_TEST_ID"))
            db_path: str = "dbTest.json"
            self.bot_id: int = int(os.getenv("BOT_TEST_ID"))
        else:
            self.bot_id: int = int(os.getenv("BOT_ID"))
            self.token: str = os.getenv("TOKEN")
            self.guild_id: int = int(os.getenv("GUILD_ID"))
            db_path: str = "db.json"
        super().__init__("!", intents=Intents.all(), application_id=self.bot_id)
        DbHandler.__init__(self, db_path)
        self.is_test_mode: bool = is_test_mode
        self.riot_token: str = os.getenv("RIOT_API_KEY")

userList = NewType("userList", List[User])
