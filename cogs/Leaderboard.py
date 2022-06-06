from discord.ext import commands
from discord import app_commands, Interaction, Object


from commands.leaderboard import refresh
from commands.leaderboard import register


from utils.myTypes import Setup


class Leaderboard(commands.Cog, description="Groupe de commandes du Leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="register", description="Ajouter/Changer son compte lié au Serveur")
    async def register(self, ctx: Interaction, summoner_name: str):
        await register.register(self.bot, ctx)

    @register.error
    async def registerError(self, ctx: Interaction, error: Exception):
        await ctx.send(f"{error}", ephemeral=True)

    @app_commands.command(name="refresh", description="Rafraichir le Leaderboard")
    @app_commands.checks.has_role("bot admin")
    async def refresh(self, ctx: Interaction):
        await refresh.refresh(self.bot, ctx)

    @refresh.error
    async def refreshError(self, ctx: Interaction, error: Exception):
        await ctx.send(f"Vous n'avez pas les permissions nécessaires pour effectuer cette action !", ephemeral=True)


async def setup(bot: Setup):
    await bot.add_cog(Leaderboard(bot), guilds=[Object(id=bot.guild_id)])