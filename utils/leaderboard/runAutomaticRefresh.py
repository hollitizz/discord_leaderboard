import asyncio
import traceback

from utils.leaderboard.refresh import loopedRefresh

async def set_interval(sec = 300, fct = loopedRefresh):
    while True:
        try:
            await fct()
        except:
            traceback.print_exc()
        await asyncio.sleep(sec)

async def runAutomaticRefresh():
    loop = asyncio.get_event_loop()
    loop.create_task(set_interval())