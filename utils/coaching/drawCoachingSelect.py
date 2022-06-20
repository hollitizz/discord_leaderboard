import random
import discord
from dateutil import tz

from utils.getChannelByName import getChannelByName

class drawCoachingSelect(discord.ui.Select):
    def __init__(self, bot, events):
        super().__init__(
            placeholder="Choisis l'évenement cible",
            options=[
                discord.SelectOption(
                    label=f"{event.name} le {event.start_time.astimezone(tz=tz.gettz('Europe/Paris')).strftime('%d/%m/%Y à %H:%M')}",
                    value= str(i),
                ) for i, event in enumerate(events)
            ]
        )
        self.events = events
        self.bot = bot

    async def callback(self, ctx: discord.Interaction):
        index = int(self.values[0])
        user_list = []
        [user_list.append(user) async for user in self.events[index].users()]
        start_time = self.events[index].start_time.astimezone(tz=tz.gettz('Europe/Paris')).strftime('%d/%m/%Y à %H:%M')
        if not user_list:
            raise Exception("Il n'y a pas de participants pour cet évènement")
        choice = random.choice(user_list).mention
        msg = await getChannelByName(self.bot, "coaching").send(f"{choice} à été chosis pour le coaching !\n"
            f"rendez-vous le {start_time} !")
        await ctx.response.edit_message(content=msg.jump_url, view=None)

class drawCoachingView(discord.ui.View):
    def __init__(self, bot, events):
        super().__init__()
        self.add_item(drawCoachingSelect(bot, events))