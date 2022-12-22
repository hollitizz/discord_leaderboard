from asyncio import sleep
from utils.leaderboard.getPlayerStats import getPlayerStats
from utils.myTypes import Setup
from logging import getLogger


_logger = getLogger(__name__)


async def refreshStats(self: Setup):
    users_id = self.db.getUsersId()

    for i, user_id in enumerate(users_id):
        if ((i + 1) % 100 == 0):
            _logger.info("Sleeping for 60 seconds")
            await sleep(1)
        try:
            tier, rank, lp, summoner_name = await getPlayerStats(self.riot_token, user)
            self.db.updateUser(user_id, tier, rank, lp, summoner_name)
            _logger.info(f"Stats of {summoner_name} refreshed")
        except Exception as e:
            _logger.error(f"Error while refreshing stats of {summoner_name}: {e}")
            continue
