from discord.ext.commands import Cog
from discord import app_commands, Interaction
from commands.leaderboard import refresh
from commands.leaderboard import register

from utils.Setup import Setup

class Leaderboard(Cog, description="Group of commands for the leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="refresh", description="Refresh the leaderboard")
    async def refresh(self, ctx: Interaction):
        await refresh.refresh(self.bot, ctx)

    @app_commands.command(name="register", description="Register to the leaderboard")
    async def register(self, ctx: Interaction):
        await register.register(self.bot, ctx)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))