from discord.ext import commands
from discord import app_commands, Interaction

from commands.diverse import ping
from utils.Setup import Setup


class Diverse(commands.Cog, description="Group of commands for the leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="ping", description="Reply with Pong")
    async def slashPing(self, ctx: Interaction):
        await ping.ping(ctx)

async def setup(bot):
    await bot.add_cog(Diverse(bot))