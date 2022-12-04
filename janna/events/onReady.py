import discord

from utils.myTypes import Setup
import logging

async def onReady(self: Setup):
    await self.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="League of Legends"
        )
    )
    logging.info(f"{self.user} is Ready !")
