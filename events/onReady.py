import discord

from utils.leaderboard.runAutomaticRefresh import runAutomaticRefresh
from utils.myTypes import Setup


async def onReady(self: Setup):
    await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="League of Legends"))
    print(f"{self.user} is Ready !")
    # await runAutomaticRefresh(self)