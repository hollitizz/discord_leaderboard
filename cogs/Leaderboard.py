from discord.ext import commands
from discord_slash import cog_ext

from commands.Leaderboard import refresh

from utils.Setup import Setup

class Leaderboard(commands.Cog, description="Group of commands for the leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @cog_ext.cog_slash(name="Refresh", description="Refresh leaderboard")
    async def refresh(self, ctx: commands.Context):
        await refresh.refresh(ctx)

def setup(bot):
    bot.add_cog(Leaderboard(bot))