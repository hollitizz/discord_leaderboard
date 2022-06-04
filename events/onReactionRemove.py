async def onReactionRemove(self, reaction, user):
    coaching = self.db.coaching
    if reaction.message.id != coaching.message or user.bot:
        return
    coaching.participants.remove(user.mention)
    self.db.save()
    return self