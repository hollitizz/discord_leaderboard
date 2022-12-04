import logging
import sys
from discord.ext import commands
from discord import app_commands, Interaction, Object
from commands.leaderboard import refresh
from utils.myTypes import Setup


_logger = logging.getLogger(__name__)


class Leaderboard(commands.Cog, description="Groupe de commandes du Leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="refresh", description="Rafraichis le Leaderboard")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_role("bot admin")
    async def refresh(self, ctx: Interaction):
        await refresh.refresh(self.bot, ctx)

    @refresh.error
    async def refreshError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"Vous n'avez pas les permissions nécessaires pour effectuer cette action !", ephemeral=True)
        _logger.error(f"{ctx.user} got : {error}", file=sys.stderr)



async def setup(bot: Setup):
    await bot.add_cog(Leaderboard(bot), guilds=[Object(id=bot.guild_id)])
