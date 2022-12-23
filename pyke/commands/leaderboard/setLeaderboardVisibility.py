from discord import Interaction
from utils.myTypes import Setup


async def setLeaderboardVisibility(self: Setup, ctx: Interaction, visible: bool):
    self.db.setVisiblity(ctx.user.id, visible)
    if visible:
        await ctx.response.send_message("Ta devrais apparaître dans le leaderboard d'ici 10 minutes !", ephemeral=True)
    else:
        await ctx.response.send_message("Ta devrais disparaître du leaderboard d'ici 10 minutes !", ephemeral=True)
        