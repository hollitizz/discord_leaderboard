from datetime import datetime
from utils.leaderboard.refreshRoles import refreshRoles
from utils.leaderboard.refreshStats import refreshStats
from utils.leaderboard.sortLeaderboard import sortLeaderboard

import logging

_logger = logging.getLogger(__name__)


async def loopedRefresh(self):
    _logger.info("Refreshing Stats...")
    await refreshStats(self)
    _logger.info("Sorting Leaderboard...")
    await sortLeaderboard(self)
    _logger.info("Refreshing Roles...")
    await refreshRoles(self)
    _logger.info("Refresh Done !")

