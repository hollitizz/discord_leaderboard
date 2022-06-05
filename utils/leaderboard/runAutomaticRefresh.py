import asyncio
import traceback

from commands.leaderboard.refresh import loopedRefresh
from utils.myTypes import Setup

async def set_interval(sec = 300, fct = loopedRefresh, self = None):
    while True:
        try:
            await fct(self)
        except:
            traceback.print_exc()
        await asyncio.sleep(sec)

async def runAutomaticRefresh(self: Setup):
    loop = asyncio.get_event_loop()
    loop.create_task(set_interval(self=self))