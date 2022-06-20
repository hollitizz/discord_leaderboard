from discord import Message
from utils.leaderboard.addPlayerOpgg import addPlayerOpgg
from utils.leaderboard.checkOpggLinkIsValid import checkOpggLinkIsValid
from utils.myTypes import Setup


async def onMessage(self: Setup, message: Message):
    if message.channel.id in self.db.opgg_channels and checkOpggLinkIsValid(message):
        await addPlayerOpgg(self, message)