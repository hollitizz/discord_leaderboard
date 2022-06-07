from discord.ext import commands
from discord import app_commands, Interaction, Object


from commands.leaderboard import refresh
from commands.leaderboard import register

from utils.leaderboard import refreshRoles

from utils.myTypes import Setup


class Leaderboard(commands.Cog, description="Groupe de commandes du Leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="register", description="Ajouter/Changer son compte lié au Serveur")
    async def register(self, ctx: Interaction, summoner_name: str):
        await register.register(self.bot, ctx, summoner_name)

    @register.error
    async def registerError(self, ctx: Interaction, error: Exception):
        print(f"{error}")

    @app_commands.command(name="refresh", description="Rafraichis le Leaderboard")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_role("bot admin")
    async def refresh(self, ctx: Interaction):
        await refresh.refresh(self.bot, ctx)

    @refresh.error
    async def refreshError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"Vous n'avez pas les permissions nécessaires pour effectuer cette action !", ephemeral=True)

    @app_commands.command(name="refresh_roles", description="Rafraichis les roles")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_role("bot admin")
    async def refreshRolesCommand(self, ctx: Interaction):
        await refreshRoles.refreshRoles(self.bot)

    @refresh.error
    async def refreshError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"Vous n'avez pas les permissions nécessaires pour effectuer cette action !", ephemeral=True)

    @app_commands.command(name="sim_join", description="Fake event on_member_add")
    # @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_role("bot admin")
    async def simJoin(self, ctx: Interaction):
        await ctx.response.send_message(f"Fake event on_member_add", ephemeral=True)
        self.bot.dispatch("member_add", ctx.user)

    @simJoin.error
    async def simJoinError(self, ctx: Interaction, error: Exception):
        print(error)
        await ctx.response.send_message(f"Vous n'avez pas les permissions nécessaires pour effectuer cette action !", ephemeral=True)

async def setup(bot: Setup):
    await bot.add_cog(Leaderboard(bot), guilds=[Object(id=bot.guild_id)])