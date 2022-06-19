import datetime
from discord.ext import commands
from discord import app_commands, Interaction, Object
from commands.coaching import createCoaching

from commands.diverse import ping
from commands.diverse import changeRole
from utils.myTypes import Setup


class Coaching(commands.Cog, description="Groupe de commande Coaching"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="create_coaching", description="Permet de créer un coaching")
    @app_commands.checks.has_role("Coach")
    @app_commands.describe(
        date="Date du coaching, format: **jj/mm/aaaa à hh:mm** (Exemple: **19/06/2022 à 21h00**)",
        nombre_de_participants="Le nombre de personne que tu souhaite coach, par defaut à 1",
        image_url="L'url de l'image affiché sur la fiche de l'évenement, par defaut ta photo de profil",
        organisateur="L'organisateur du coaching, par defaut toi",
    )
    async def createCoaching(self, ctx: Interaction, date: str, nombre_de_participants: int = 1, image_url: str = None, organisateur: str = None):
        await createCoaching.createCoaching(self, ctx, date, nombre_de_participants, image_url, organisateur)

    @createCoaching.error
    async def createCoachingError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"{error}", ephemeral=True)

async def setup(bot: Setup):
    await bot.add_cog(Coaching(bot), guilds=[Object(id=bot.guild_id)])