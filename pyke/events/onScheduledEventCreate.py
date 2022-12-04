from discord import Guild, ScheduledEvent
from utils.getChannelByName import getChannelByName

from utils.myTypes import Setup


async def onScheduledEventCreate(self: Setup, event: ScheduledEvent):
    guild: Guild = self.get_guild(self.guild_id)
    if event.name.startswith("Session de Coaching"):
        channel = getChannelByName(self, "coaching")
        if channel:
            await channel.send(f"Hello <@&913831403811110932> !\n Il y a un nouveau coaching de disponible n'hésitez pas a vous inscrire ! :\n{event.url}")

