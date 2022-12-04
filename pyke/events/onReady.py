import discord
import logging
from utils.myTypes import Setup


_logger = logging.getLogger(__name__)


async def onReady(self: Setup):
    await self.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="League of Legends"
        )
    )
    _logger.info(f"{self.user} is Ready !")
