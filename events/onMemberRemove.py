from utils.leaderboard.checkPlayerExist import checkPlayerExist

async def onMemberRemove(self, member):
    tag = member.mention
    pos = checkPlayerExist(self.db.leaderboard.users, tag)
    if (pos == -1):
        return
    print(f"{self.db.leaderboard.users.pop(pos)} Poped !: Reason: {member} left the server")
    self.Db.save()
    return self