import discord
from dateutil import tz

class drawCoachingSelect(discord.ui.Select):
    def __init__(self, events):
        super().__init__(
            options=[
                discord.SelectOption(
                    label=f"{i}. {event.name} le {event.start_time.astimezone(tz=tz.gettz('Europe/Paris')).strftime('%d/%m/%Y à %H:%M')}",
                    default=True if i == 1 else False
                ) for i, event in enumerate(events, 1)
            ]
        )