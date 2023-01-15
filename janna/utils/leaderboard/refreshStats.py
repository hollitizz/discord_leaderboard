import traceback
from utils.leaderboard.getPlayerStats import getPlayerStats
from utils.myTypes import Setup
from logging import getLogger


_logger = getLogger(__name__)


async def refreshStats(self: Setup):
    users_id = self.db.getUsersId()

    for user_id in users_id:
        for summoner_name, league_id in self.db.getUserAccountsLeagueId(user_id):
            try:
                tier, rank, lp, summoner_name = await getPlayerStats(self.riot_token, league_id, summoner_name)
                self.db.updateUser(league_id, tier, rank, lp, summoner_name)
            except Exception as e:
                traceback.print_exc()
                _logger.error(f"Error while refreshing stats of {summoner_name}: {e}")
                continue
