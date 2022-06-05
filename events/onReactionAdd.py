from discord import Reaction, User

from utils.myTypes import Setup

async def onReactionAdd(self: Setup, reaction: Reaction, user: User):
    coaching = self.db.coaching
    if reaction.message.id != coaching.message or user.bot:
        return self
    coaching.participants.append(user.mention)
    self.db.save()
    return self