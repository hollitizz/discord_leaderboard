from utils.leaderboard.checkIdExist import checkIdExist


async def setLeaderboardVisibility(self, ctx, visible):
    pos = checkIdExist(self.bot.db.leaderboard.users, ctx.user.mention)
    if pos == -1:
        raise Exception("Tu n'es pas enregistré sur le leaderboard !")
    self.bot.db.leaderboard.users[pos].is_displayed = visible
    self.bot.save()
    ctx.response.send_message("Ta visibilité sur le Leaderboard a été mis à jour !")