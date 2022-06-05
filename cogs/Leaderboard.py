from discord.ext import commands
from discord import app_commands, Interaction, Object
from commands.leaderboard import refresh
from commands.leaderboard import register
from utils.checkPerms import checkPerms

from utils.myTypes import Setup

class Leaderboard(commands.Cog, description="Groupe de commandes du Leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(
        name="new",
        description="Ajouter/Changer son compte lié au Serveur",
    )
    async def new(self, ctx: Interaction, summoner_name: str):
        await register.register(self.bot, ctx)

    @app_commands.command(name="refresh", description="Rafraichir le Leaderboard")
    async def refresh(self, ctx: Interaction):
        checkPerms(self.bot, ctx)
        await refresh.refresh(self.bot, ctx)

    @refresh.error
    async def refreshError(self, ctx: Interaction, error: Exception):
        await ctx.send(f"{error}", ephemeral=True)


async def setup(bot: Setup):
    await bot.add_cog(Leaderboard(bot), guilds=[Object(id=bot.guild_id)])