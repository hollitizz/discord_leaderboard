import random
import discord
from discord.ext import commands
from discord import Guild, Member, ScheduledEvent, app_commands, Interaction, Object
from commands.coaching import createCoaching
from dateutil import tz
from utils.coaching.drawCoachingSelect import drawCoachingSelect
from utils.getChannelByName import getChannelByName
from utils.myTypes import Setup


class Coaching(commands.Cog, description="Groupe de commande Coaching"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="create_coaching", description="Permet de créer un coaching")
    @app_commands.checks.has_role("Coach")
    @app_commands.describe(
        date="Date du coaching, format: **jj/mm/aaaa à hh:mm** (Exemple: **19/06/2022 à 21:00**)",
        nombre_de_participants="Le nombre de personne que tu souhaite coach, par defaut à 1",
        image_url="L'url de l'image affiché sur la fiche de l'évenement, par defaut ta photo de profil",
        organisateur="L'organisateur du coaching, par defaut toi",
    )
    async def createCoaching(self, ctx: Interaction, date: str, nombre_de_participants: int = 1, image_url: str = None, organisateur: Member = None):
        await createCoaching.createCoaching(self, ctx, date, nombre_de_participants, image_url, organisateur)

    @createCoaching.error
    async def createCoachingError(self, ctx: Interaction, error: Exception):
        await ctx.response.send_message(f"{error}", ephemeral=True)

    @app_commands.command(name="draw_coaching", description="Tire au sort un personne pour le coaching")
    async def drawCoaching(self, ctx: Interaction, organisateur: Member = None):
        if not organisateur:
            organisateur = ctx.user
        await ctx.response.defer(thinking=True, ephemeral=True)
        guild: Guild = self.bot.get_guild(self.bot.guild_id)
        user_events: list(ScheduledEvent) = []
        for event in guild.scheduled_events:
            if organisateur.name.lower() in event.name.lower():
                user_events.append(event)
        if len(user_events) > 1:
            msg: list(str) = []
            view = discord.ui.View()
            view.add_item(drawCoachingSelect(user_events))
            await ctx.edit_original_message(content=f"Choisissez l'event :", view=view)
            wanted_event_index = await self.bot.wait_for("message", check=lambda m: m.author == organisateur and m.channel == ctx.channel)
            await wanted_event_index.delete()
        else:
            wanted_event_index = 1
        user_list = []
        if wanted_event_index:
            [user_list.append(user) async for user in user_events[int(wanted_event_index.content) - 1].users()]
            start_time = user_events[int(wanted_event_index.content) - 1].start_time.astimezone(tz=tz.gettz('Europe/Paris')).strftime('%d/%m/%Y à %H:%M')
        await getChannelByName(self.bot, "coaching").send(f"{random.choice(user_list).mention} à été chosis pour le coaching !\n"
        f"rendez-vous le {start_time} !")

async def setup(bot: Setup):
    await bot.add_cog(Coaching(bot), guilds=[Object(id=bot.guild_id)])