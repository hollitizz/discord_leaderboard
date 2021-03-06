import sys
from discord.ext import commands
from discord import Member, app_commands, Interaction, Object
from discord.app_commands import Choice


from commands.leaderboard import refresh, register, addPlayer, setLeaderboardVisibility

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
        await ctx.response.send_message(f"{error.args[0]}")
        print(f"{ctx.user} got : {error}", file=sys.stderr)

    @app_commands.command(name="refresh", description="Rafraichis le Leaderboard")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_role("bot admin")
    async def refresh(self, ctx: Interaction):
        await refresh.refresh(self.bot, ctx)

    @refresh.error
    async def refreshError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"Vous n'avez pas les permissions nécessaires pour effectuer cette action !", ephemeral=True)
        print(f"{ctx.user} got : {error}", file=sys.stderr)

    @app_commands.command(name="refresh_roles", description="Rafraichis les roles")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_role("bot admin")
    async def refreshRoles(self, ctx: Interaction):
        await ctx.response.defer(thinking=True, ephemeral=True)
        await refreshRoles.refreshRoles(self.bot)
        await ctx.edit_original_message(content="Roles rafraichis !")

    @refreshRoles.error
    async def refreshRolesError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"Vous n'avez pas les permissions nécessaires pour effectuer cette action !", ephemeral=True)
        print(f"{ctx.user} got : {error}", file=sys.stderr)

    @app_commands.command(name="add_player", description="Ajoute un joueur au Leaderboard")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_role("bot admin")
    async def addPlayer(self, ctx: Interaction, membre: Member, summoner_name: str):
        await addPlayer.addPlayer(self.bot, ctx, membre, summoner_name)

    @addPlayer.error
    async def addPlayerError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"{error.args[0]}", ephemeral=True)
        print(f"{ctx.user} got : {error}", file=sys.stderr)

    @app_commands.command(name="set_leaderboard_visibility", description="Choisis si tu veux apparaître dans le Leaderboard")
    @app_commands.choices(visible=[Choice(name="Apparaître", value=1), Choice(name="Ne pas apparaître", value=0)])
    async def setLeaderboardVisibility(self, ctx: Interaction, visible: int):
        await setLeaderboardVisibility.setLeaderboardVisibility(self, ctx, bool(visible))

    @setLeaderboardVisibility.error
    async def setLeaderboardVisibilityError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"{error.args[0]}", ephemeral=True)
        print(f"{ctx.user} got : {error}", file=sys.stderr)


async def setup(bot: Setup):
    await bot.add_cog(Leaderboard(bot), guilds=[Object(id=bot.guild_id)])
