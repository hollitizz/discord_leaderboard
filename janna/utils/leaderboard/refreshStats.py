from asyncio import sleep
from utils.leaderboard.getPlayerStats import getPlayerStats
from utils.myTypes import Setup
from logging import getLogger


_logger = getLogger(__name__)


async def refreshStats(self: Setup):
    users = self.db.getUsersId()

    for i, user in enumerate(users):
        if ((i + 1) % 10 == 0):
            await sleep(1)
        try:
            user = await getPlayerStats(self.riot_token, user)
        except Exception as e:
            _logger.error(f"Error while refreshing stats for {user}: {e}")
            continue
