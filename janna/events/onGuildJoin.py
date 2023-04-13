from discord import Guild
from utils.myTypes import Setup
import logging


_logger = logging.getLogger(__name__)


async def onGuildJoin(self: Setup, guild: Guild):
    _logger.info(f"Joined guild {guild.name} (id: {guild.id})")
