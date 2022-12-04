from utils.leaderboard.checkIdExist import checkIdExist
from utils.leaderboard.refreshRoles import refreshUserRole
from utils.myTypes import User, Setup


async def createPlayer(self: Setup, user: User):
    users = self.db.leaderboard.users
    player_exist = checkIdExist(users, user.tag)
    if (player_exist == -1):
        users.append(user)
    else:
        users[player_exist] = user
    guild = self.get_guild(self.guild_id)
    await refreshUserRole(guild, user)
    self.save()