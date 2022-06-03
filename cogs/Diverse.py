from discord.ext import commands
from discord_slash import cog_ext

from commands import ping

class Diverse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name="ping", description="Ping the bot", usage="ping")
    # async def commandPing(self, ctx):
    #     await ping.commandPing(ctx)

    @cog_ext.cog_slash(name="Ping", description="reply with pong")
    async def slashPing():
        await ping.slashPing()
