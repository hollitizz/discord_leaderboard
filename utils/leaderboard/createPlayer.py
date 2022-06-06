from utils.leaderboard.checkIdExist import checkIdExist
from utils.leaderboard.checkName import checkName
from utils.myTypes import User, Setup


async def createPlayer(self: Setup, user: User):
    users = self.db.leaderboard.users
    leaderboard = self.db.leaderboard
    leaderboard.tmp_id = await checkName(users, leaderboard.tmp_id)
    player_exist = checkIdExist(user.tag)
    if (not leaderboard.tmp_id):
        return
    if (player_exist == -1):
        users.append(user)
    else:
        users[player_exist] = user
    leaderboard.tmp_id = None
    self.save()