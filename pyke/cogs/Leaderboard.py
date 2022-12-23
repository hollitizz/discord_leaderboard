import sys
import traceback
from discord.ext import commands
from discord import Member, app_commands, Interaction, Object
from discord.app_commands import Choice

import logging
from commands.leaderboard import register, addPlayer, setLeaderboardVisibility
from utils.myTypes import Setup


_logger = logging.getLogger(__name__)


class Leaderboard(commands.Cog, description="Groupe de commandes du Leaderboard"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="register", description="Ajouter/Changer son compte lié au Serveur")
    async def register(self, ctx: Interaction, summoner_name: str):
        _logger.info(f"{ctx.user} used  /{ctx.command.name} with ['{summoner_name}'] as arguments")
        await register.register(self.bot, ctx, summoner_name)

    @register.error
    async def registerError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message("an error occured !", ephemeral=True)
        _logger.error(f"{ctx.user} got : {error}")
        traceback.print_exc()

    @app_commands.command(name="add_player", description="Ajoute un joueur au Leaderboard")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_role("bot admin")
    async def addPlayer(self, ctx: Interaction, membre: Member, summoner_name: str):
        _logger.info(f"{ctx.user} used  /{ctx.command.name} with ['{membre}', '{summoner_name}'] as arguments")
        await addPlayer.addPlayer(self.bot, ctx, membre, summoner_name)

    @addPlayer.error
    async def addPlayerError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"an error occured", ephemeral=True)
        _logger.error(f"{ctx.user} got : {error}")
        traceback.print_exc()

    @app_commands.command(name="set_leaderboard_visibility", description="Choisis si tu veux apparaître dans le Leaderboard")
    @app_commands.choices(visible=[Choice(name="Apparaître", value=1), Choice(name="Ne pas apparaître", value=0)])
    async def setLeaderboardVisibility(self, ctx: Interaction, visible: int):
        _logger.info(f"{ctx.user} used  /{ctx.command.name} with ['{visible}'] as arguments")
        await setLeaderboardVisibility.setLeaderboardVisibility(self.bot, ctx, bool(visible))

    @setLeaderboardVisibility.error
    async def setLeaderboardVisibilityError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"an error occured", ephemeral=True)
        _logger.error(f"{ctx.user} got : {error}")
        traceback.print_exc()


async def setup(bot: Setup):
    await bot.add_cog(Leaderboard(bot), guilds=[Object(id=bot.guild_id)])
