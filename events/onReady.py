from utils.Setup import Setup
from utils.leaderboard.runAutomaticRefresh import runAutomaticRefresh


async def onReady(self: Setup):
    print(f"{self.user} is Ready !")
    await runAutomaticRefresh()