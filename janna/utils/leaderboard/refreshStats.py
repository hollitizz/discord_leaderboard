from asyncio import sleep
from utils.leaderboard.getPlayerStats import getPlayerStats
from utils.myTypes import Setup


async def refreshStats(self: Setup):
    users = self.db.getUsers()

    for i, user in enumerate(users):
        if ((i + 1) % 10 == 0):
            sleep(1)
        try:
            user = await getPlayerStats(self.riot_token, user)
        except:
            continue
    self.save()