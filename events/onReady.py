from utils.leaderboard.runAutomaticRefresh import runAutomaticRefresh
from utils.myTypes import Setup


async def onReady(self: Setup):
    print(f"{self.user} is Ready !")
    await runAutomaticRefresh(self)