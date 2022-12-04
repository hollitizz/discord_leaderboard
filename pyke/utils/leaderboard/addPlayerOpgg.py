import urllib
from discord import Message
from utils.leaderboard.checkName import checkName
from utils.myTypes import User, Setup

from utils.leaderboard.createPlayer import createPlayer


async def addPlayerOpgg(self: Setup, message: Message):
    leaderboard = self.db.leaderboard
    tag = message.author.mention
    tmp = message.content.split()
    if len(tmp) == 2 and tmp[1].startswith("<@"):
        tag = tmp[1]
    opgg = tmp[0].split("/")
    opgg = opgg[-1].split("=")
    user = urllib.parse.unquote(opgg[-1])
    new_user = User(tag, user, checkName(user))
    await new_user.setStats(self.riot_token)
    await createPlayer(self, new_user)
