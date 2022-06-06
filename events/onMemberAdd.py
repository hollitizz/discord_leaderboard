from discord import Member
from utils.leaderboard.checkIdExist import checkIdExist
from utils.leaderboard.checkName import checkName
from utils.leaderboard.createPlayer import createPlayer
from utils.myTypes import Setup, User
from utils.leaderboard.refreshStats import API_RANK
from utils.leaderboard.refreshRoles import ROLE_LIST, getRoleByName

def getBotTier(tier: int):
    for tier_api, tier_int in ROLE_LIST.items():
        if tier_api == tier:
            return tier_int


def getBotRank(rank: int):
    for rank_api, rank_int in API_RANK.items():
        if rank_int == rank:
            return rank_api


async def askNewMember(self: Setup, member: Member):
    tag = member.mention
    await member.send(f"Salut, d'abord merci d'avoir rejoint le serveur !\n"\
                f"Pour continuer, peux-tu tout d'abord m'envoyer ton nom d'invocateur (pseudo sur league), verifie bien que tu soit en EUW\n")
    while True:
        summoner_name = await self.wait_for("message", check=lambda m: m.author == member)
        summoner_id = checkName(summoner_name)
        if summoner_id:
            break
    new_User = User(tag, summoner_id, summoner_id)
    new_User.setStats(self.riot_token)
    tier = getBotTier(new_User.tier)
    rank = getBotRank(new_User.rank)
    msg = "Tu es actuellement **{tier}"
    if tier != "Unranked":
        msg += f" {rank} {new_User.lp}lp"
    msg += "**, si ce n'est pas le cas met un demande a <@222008900025581568> de t'aider"
    return new_User


async def onMemberAdd(self: Setup, member: Member):
    tag = member.mention
    new_member_role = getRoleByName("Nouveau")
    await member.add_roles(new_member_role)
    pos = await checkIdExist(self.db.leaderboard.users, tag)
    if (pos == -1):
        newUser = askNewMember()
        createPlayer(self, askNewMember())
    await member.remove_roles(new_member_role)
