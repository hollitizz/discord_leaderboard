from utils.leaderboard.sortLeaderboard import printLeaderboard
from utils.leaderboard.refreshRoles import refreshRoles
from utils.leaderboard.refreshStats import refreshStats

import logging

_logger = logging.getLogger(__name__)


async def loopedRefresh(self):
    _logger.info("Refreshing Stats...")
    await refreshStats(self)
    _logger.info("Refreshing Leaderboard...")
    await printLeaderboard(self)
    _logger.info("Refreshing Roles...")
    await refreshRoles(self)
    _logger.info("Refresh Done !")

