from discord import Guild
from utils.myTypes import Setup
import logging


_logger = logging.getLogger(__name__)


async def onGuildLeave(self: Setup, guild: Guild):
    _logger.info(f"Leave guild {guild.name} (id: {guild.id})")
