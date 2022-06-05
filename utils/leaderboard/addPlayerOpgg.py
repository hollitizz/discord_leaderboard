import urllib
from discord import Message
from utils.myTypes import User, Setup

from utils.leaderboard.createPlayer import create_player


async def addPlayerOpgg(self: Setup, message: Message):
    leaderboard = self.db.leaderboard
    tag = message.author.mention
    tmp = message.content.split()
    if len(tmp) == 2 and tmp[1].startswith("<@"):
        tag = tmp[1]
    opgg = tmp[0].split("/")
    opgg = opgg[-1].split("=")
    user = urllib.parse.unquote(opgg[-1])
    create_player(self, User(tag, user, leaderboard.tmp_id))
