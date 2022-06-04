from discord.ext import commands
from discord_slash import cog_ext


from commands.Diverse import ping


class Diverse(commands.Cog, description="Group of commands for the leaderboard"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Reply with Pong", usage="ping")
    async def commandPing(self, ctx):
        await ping.commandPing(ctx)

    @cog_ext.cog_slash(name="Ping", description="Reply with Pong")
    async def slashPing(self, ctx):
        await ping.slashPing(ctx)
