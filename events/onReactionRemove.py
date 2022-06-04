from utils.Setup import Setup
from discord import Reaction, User

async def onReactionRemove(self: Setup, reaction: Reaction, user: User):
    coaching = self.db.coaching
    if reaction.message.id != coaching.message or user.bot:
        return
    coaching.participants.remove(user.mention)
    self.db.save()
    return self