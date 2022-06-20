
from discord import Guild, Interaction, ScheduledEvent

from utils.coaching.drawCoachingSelect import drawCoachingView


async def drawCoaching(self, ctx: Interaction):
    user = ctx.user
    if user.guild_permissions.administrator:
        see_all = True
    else:
        see_all = False
    await ctx.response.defer(thinking=True, ephemeral=True)
    guild: Guild = self.bot.get_guild(self.bot.guild_id)
    user_events: list(ScheduledEvent) = []
    for event in guild.scheduled_events:
        if event.name.startswith("Session de Coaching") and (user.name.lower() in event.name.lower() or see_all):
            user_events.append(event)
    if not user_events:
        raise Exception("Tu n'a pas encore créé d'évènement de coaching. Tu peux utiliser la commande `create_coaching` pour en créer un !")
    await ctx.edit_original_message(content="", view=drawCoachingView(self.bot, user_events))