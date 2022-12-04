from datetime import datetime, timedelta
import io
from PIL import Image
from discord import ChannelType, EntityType, Guild, Interaction
from dateutil import tz
import requests
from utils.getChannelByName import getChannelByName

async def createCoaching(self, ctx: Interaction, date: str, nombre_de_participants: int, image_url: str, organisateur: str):
    if not image_url:
        image_url = ctx.user.avatar.url
    if not organisateur:
        organisateur = ctx.user.name
    guild: Guild = self.bot.get_guild(self.bot.guild_id)
    formated_date: datetime = datetime.strptime(date, '%d/%m/%Y à %H:%M')
    formated_date = formated_date.astimezone(tz=tz.gettz("Europe/Paris"))
    msg =   f"{ctx.user.mention} organise un coaching **{date}**\n"\
            f"cliquer sur **intéressé** pour vous inscrire"\
            f" et attend de voir le résultat, {nombre_de_participants} personne(s) tirée(s) au sort"
    channel = getChannelByName(self.bot, "coaching", ChannelType.voice)
    if not channel:
        raise Exception("Je n'ai pas réussi à trouver le channel vocal 'coaching'")
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content), mode="r")
    b = io.BytesIO()
    img.save(b, format="PNG")
    event = await guild.create_scheduled_event(
        name=f"Session de Coaching par {ctx.user.name}",
        description=msg,
        channel=channel,
        image=b.getvalue(),
        start_time=formated_date,
        end_time=formated_date + timedelta(hours=1),
        entity_type=EntityType.voice,
    )
    await ctx.response.send_message(f"Tu as créé un coaching le {date}", ephemeral=True)
