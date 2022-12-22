import sys
from typing import List
from discord.ext import commands
from discord import app_commands, Interaction, Object
import logging
from commands.diverse import ping, changeRole, roll, getOpgg, uwu
from utils.myTypes import Setup


_logger = logging.getLogger(__name__)


class Diverse(commands.Cog, description="Groupe de commande Divers"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="ping", description="Répond avec \"Pong !\"")
    async def ping(self, ctx: Interaction):
        _logger.info(f"{ctx.user} used /{ctx.command.name} with no arguments")
        await ping.ping(ctx)

    @app_commands.command(name="change_role", description="Te permet de changer ton main role")
    async def changeRole(self, ctx: Interaction):
        _logger.info(f"{ctx.user} used /{ctx.command.name} with no arguments")
        await changeRole.changeRole(self, ctx)

    @changeRole.error
    async def changeRoleError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message("An error occurded", ephemeral=True)
        _logger.error(f"{ctx.user} got : {error}")

    @app_commands.command(name="roll", description="Récuperer un nombre random entre deux int")
    @app_commands.describe(min="borne inférieure, 1 par defaut", max="borne supérieure, 6 par défaut")
    async def roll(self, ctx: Interaction, min: int=1, max: int=6):
        _logger.info(f"{ctx.user} used /{ctx.command.name} with ['{min}', '{max}'] arguments")
        await roll.roll(self, ctx, min, max)

    @app_commands.command(name="roll_in_list", description="recuperer une string random dans une liste")
    @app_commands.describe(
        liste = "la liste de string parmis laquelle tu veux faire ton tirage",
        separateur = "caractère séparant les chaînes de caractères, par defaut un espace"
    )
    async def rollInList(self, ctx: Interaction, liste: str, separateur:str = " "):
        _logger.info(f"{ctx.user} used  /{ctx.command.name} with ['{liste}', '{separateur}'] as arguments")
        await roll.rollInList(self, ctx, liste, separateur)

    @app_commands.command(name="get_opgg", description="Recuperer le opgg d'un ou plusieurs joueurs")
    @app_commands.describe(liste="Mention du joueur voulu/Liste de mention de joueur", séparateur="caractère séparant les mentions, par defaut un espace")
    async def getOpgg(self, ctx: Interaction, liste: str, separateur: str = " "):
        _logger.info(f"{ctx.user} used  /{ctx.command.name} with ['{liste}', '{separateur}'] as arguments")
        await getOpgg.getOpgg(self.bot, ctx, liste, separateur)

    @getOpgg.error
    async def getOpggError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message("an error occured", ephemeral=True)
        _logger.error(f"{ctx.user} got : {error}", file=sys.stderr)

    @app_commands.command(name="uwu", description="Dis UwU")
    @app_commands.checks.has_role("bot admin")
    async def uwu(self, ctx: Interaction, channel: str = None):
        _logger.info(f"{ctx.user} used  /{ctx.command.name} with {'no argument' if channel is None else f'[\'{channel}\']'} arguments")
        await uwu.uwu(self, ctx, channel)

async def setup(bot: Setup):
    await bot.add_cog(Diverse(bot), guilds=[Object(id=bot.guild_id)])