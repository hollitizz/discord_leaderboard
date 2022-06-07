from discord import Member
from utils.leaderboard.checkIdExist import checkIdExist
from utils.leaderboard.checkName import checkName
from utils.leaderboard.createPlayer import createPlayer
from utils.myTypes import Setup, User
from utils.leaderboard.getPlayerStats import API_RANK
from utils.leaderboard.refreshRoles import ROLE_LIST, getRoleByName

def getBotRank(rank: int):
    for rank_api, rank_int in API_RANK.items():
        if rank_int == rank:
            return rank_api


async def askNewMember(self: Setup, member: Member):
    tag = member.mention
    await member.send(f"Salut, d'abord merci d'avoir rejoint le serveur !\n"\
                f"Pour continuer, peux-tu tout d'abord m'envoyer ton nom d'invocateur (pseudo sur league), verifie bien que tu soit en EUW\n")
    while True:
        member_message = await self.wait_for("message", check=lambda m: m.author == member)
        summoner_name = member_message.content
        summoner_id = checkName(summoner_name)
        if summoner_id:
            break
    new_user = User(tag, summoner_name, summoner_id)
    await new_user.setStats(self.riot_token)
    tier = ROLE_LIST[new_user.tier]
    rank = getBotRank(new_user.rank)
    msg = f"Tu es actuellement **{tier}"
    if tier != "Unranked":
        msg += f" {rank} {new_user.lp}lp"
    msg += "**, si ce n'est pas le cas met un demande a <@222008900025581568> de t'aider"
    await member.send(msg)
    return new_user


async def onMemberJoin(self: Setup, member: Member):
    tag = member.mention
    new_member_role = getRoleByName(member.guild, "Nouveau")
    await member.add_roles(new_member_role)
    pos = checkIdExist(self.db.leaderboard.users, tag)
    if (pos == -1):
        new_user = await askNewMember(self, member)
        await createPlayer(self, new_user)
    await member.remove_roles(new_member_role)
