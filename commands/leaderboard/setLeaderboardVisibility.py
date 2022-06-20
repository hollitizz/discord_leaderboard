from utils.leaderboard.checkIdExist import checkIdExist


async def setLeaderboardVisibility(self, ctx, visible):
    pos = checkIdExist(self.bot.db.users, ctx.user.mention)
    if pos == -1:
        raise Exception("Tu n'es pas enregistré sur le leaderboard !")
    self.bot.db.users[pos].is_displayed = visible
    self.save()
    ctx.response.send_message("Ta visibilité sur le Leaderboard a été mis à jour !")