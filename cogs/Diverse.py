from discord.ext import commands
from discord_slash import cog_ext, SlashContext


from commands.Diverse import ping
from utils.Setup import Setup


class Diverse(commands.Cog, description="Group of commands for the leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @cog_ext.cog_slash(name="Ping", description="Reply with Pong")
    async def slashPing(self, ctx: SlashContext):
        await ping.ping(ctx)

def setup(bot):
    bot.add_cog(Diverse(bot))