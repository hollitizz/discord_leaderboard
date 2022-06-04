import urllib
from utils.leaderboard.checkPlayerExist import checkPlayerExist
from utils.leaderboard.checkName import checkName


async def addPlayerOpgg(Db, message):
    users = Db.db.leaderboard.users
    leaderboard = Db.db.leaderboard
    tag = message.author.mention
    tmp = message.content.split()
    if len(tmp) == 2 and tmp[1].startswith("<@"):
        tag = tmp[1]
    player_exist = checkPlayerExist(tag)
    opgg = tmp[0].split("/")
    opgg = opgg[-1].split("=")
    user = urllib.parse.unquote(opgg[-1])
    name_exist, leaderboard.tmp_id = await checkName(users, leaderboard.tmp_id)
    if (not name_exist):
        return
    if (player_exist == -1):
        users.append([tag, user, None, None, None, leaderboard.tmp_id])
    else:
        users[player_exist] = [tag, user, None, None, None, leaderboard.tmp_id]
    leaderboard.tmp_id = None
    Db.save()
    return Db