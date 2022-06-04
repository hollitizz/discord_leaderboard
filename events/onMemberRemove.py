from discord import Member
from utils.Setup import Setup
from utils.leaderboard.checkIdExist import checkIdExist

async def onMemberRemove(self: Setup, member: Member):
    tag = member.mention
    pos = checkIdExist(self.db.leaderboard.users, tag)
    if (pos == -1):
        return
    print(f"{self.db.leaderboard.users.pop(pos)} Poped !: Reason: {member} left the server")
    self.Db.save()
    return self