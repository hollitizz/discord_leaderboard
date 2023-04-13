import discord
import logging
from utils.myTypes import Setup

_logger = logging.getLogger(__name__)


async def onMemberJoin(self: Setup, member: discord.Member):
    _logger.info(f"User \"{member}\" joined the server")
