from discord.ext import commands
from discord_slash import cog_ext


class Leaderboard(commands.Cog, description="Group of commands for the leaderboard"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="refresh", description="Refresh the leaderboard", usage="ping")
    async def commandRefresh(self, ctx):
        pass

    @cog_ext.cog_slash(name="Refresh", description="reply with pong")
    async def slashRefresh(self, ctx):
        pass
