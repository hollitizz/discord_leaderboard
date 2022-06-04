async def onReactionAdd(self, reaction, user):
    coaching = self.db.coaching
    if reaction.message.id != coaching.message or user.bot:
        return self
    coaching.participants.append(user.mention)
    self.db.save()
    return self