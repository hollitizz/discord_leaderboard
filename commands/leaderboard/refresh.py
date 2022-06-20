from time import sleep, strftime as getTime
from discord import Interaction

from utils.leaderboard.refreshRoles import refreshRoles
from utils.leaderboard.refreshStats import refreshStats
from utils.leaderboard.sortLeaderboard import sortLeaderboard

from utils.myTypes import Setup

async def loopedRefresh(self):
    print(f"[{getTime('%H:%M:%S')}]: Refreshing Stats...   ", end="\r")
    await refreshStats(self)
    print(f"[{getTime('%H:%M:%S')}]: Sorting Leaderboard...", end="\r")
    await sortLeaderboard(self)
    print(f"[{getTime('%H:%M:%S')}]: Refreshing Roles...    ", end="\r")
    if not self.is_test_mode:
        await refreshRoles(self)
    print(f"[{getTime('%H:%M:%S')}]: Refresh Done !        ")

async def refresh(self: Setup, ctx: Interaction):
    await ctx.response.defer(ephemeral=True)
    await ctx.followup.send("Refreshing Stats...")
    await refreshStats(self)
    await ctx.edit_original_message(content="Sorting Leaderboard...")
    await sortLeaderboard(self)
    await ctx.edit_original_message(content="Refresing Roles...")
    if not self.is_test_mode:
        await refreshRoles(self)
    await ctx.edit_original_message(content="Refresh Done !")