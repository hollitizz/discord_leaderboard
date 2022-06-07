import asyncio
from utils.leaderboard.getPlayerStats import getPlayerStats
from utils.myTypes import Setup, userList


async def refreshStats(self: Setup):
    users: userList = self.db.leaderboard.users

    for i, user in enumerate(users):
        if ((i + 1) % 10 == 0):
            await asyncio.sleep(1)
        try:
            user = await getPlayerStats(self.riot_token, user)
        except:
            continue
    self.save()