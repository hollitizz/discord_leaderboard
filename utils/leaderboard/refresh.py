from discord_slash import SlashContext
from Setup import Setup
from utils.leaderboard.refreshRoles import refreshRoles
from utils.leaderboard.refreshStats import refreshStats
from utils.leaderboard.sortLeaderboard import sortLeaderboard
from time import strftime as getTime

async def loopedRefresh(self: Setup):
    print("[%s]: Refreshing Stats...\r".format(getTime("%H:%M:%S")))
    refreshStats(self)
    print("[%s]: Sorting Leaderboard...\r".format(getTime("%H:%M:%S")))
    sortLeaderboard(self)
    print("[%s]: Refresing Roles...\r".format(getTime("%H:%M:%S")))
    refreshRoles(self)
    print("[%s]: Refresh Done !".format(getTime("%H:%M:%S")))

async def refresh(self: Setup, ctx: SlashContext):
    msg = await ctx.send("Refreshing Stats...", hidden=True)
    refreshStats(self)
    await msg.edit("Sorting Leaderboard...", hidden=True)
    sortLeaderboard(self)
    await msg.edit("Refresing Roles...", hidden=True)
    refreshRoles(self)
    await msg.edit("Refresh Done !", hidden=True)