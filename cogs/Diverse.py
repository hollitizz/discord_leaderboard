import sys
from typing import List
from discord.ext import commands
from discord import Member, app_commands, Interaction, Object

from commands.diverse import ping
from commands.diverse import changeRole
from commands.diverse import roll
from commands.diverse import getOpgg
from utils.myTypes import Setup


class Diverse(commands.Cog, description="Groupe de commande Divers"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="ping", description="Répond avec \"Pong !\"")
    async def ping(self, ctx: Interaction):
        await ping.ping(ctx)

    @app_commands.command(name="change_role", description="Te permet de changer ton main role")
    async def changeRole(self, ctx: Interaction):
        await changeRole.changeRole(self, ctx)

    @changeRole.error
    async def changeRoleError(self, ctx: Interaction, error: Exception):
        print(error)
        await ctx.response.send_message(
            f"Une erreur est survenue, réessaie ou sinon contacte un admin", ephemeral=True)
        print(f"{ctx.user} got : {error}", file=sys.stderr)

    @app_commands.command(name="roll", description="Récuperer un nombre random entre deux int")
    @app_commands.describe(min="borne inférieure, 1 par defaut", max="borne supérieure, 6 par défaut")
    async def roll(self, ctx: Interaction, min: int=1, max: int=6):
        await roll.roll(self, ctx, min, max)

    @app_commands.command(name="roll_in_list", description="recuperer une string random dans une liste")
    @app_commands.describe(
        liste = "la liste de string parmis laquelle tu veux faire ton tirage",
        separateur = "caractère séparant les chaînes de caractères, par defaut ' '"
    )
    async def rollInList(self, ctx, liste: str, separateur:str = " "):
        await roll.rollInList(self, ctx, liste, separateur)

    @app_commands.command(name="get_opgg", description="Recuperer le opgg d'un ou plusieurs joueurs")
    @app_commands.describe(liste="Mention du joueur voulu/Liste de mention de joueur", séparateur="caractère séparant les mentions, par defaut ' '")
    async def getOpgg(self, ctx: Interaction, liste: str, séparateur: str = " "):
        await getOpgg.getOpgg(self, ctx, liste, séparateur)

    @getOpgg.error
    async def getOpggError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"{error}", ephemeral=True)
        print(f"{ctx.user} got : {error}", file=sys.stderr)

async def setup(bot: Setup):
    await bot.add_cog(Diverse(bot), guilds=[Object(id=bot.guild_id)])