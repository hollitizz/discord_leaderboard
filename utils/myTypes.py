from typing import NewType
from utils.DbHandler import DbHandler
from discord import Intents
from discord.ext import commands

class User():
    def __init__(self, tag, name, id):
        self.tag: str = tag
        self.name: str = name
        self.tier: int = 0
        self.rank: int = 1
        self.lp: int = 0
        self.id: str = id

class Setup(commands.Bot, DbHandler):
    def __init__(self, token, riot_token):
        commands.Bot.__init__(self, "!", intents=Intents.all())
        DbHandler.__init__(self)
        self.token = token
        self.riot_token = riot_token

userList = NewType("userList", list[User])
