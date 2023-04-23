from discord import Member, TextChannel, permissions
from utils.leaderboard.refreshRoles import refreshUserRole
from utils.SQLRequests import AlreadyExists
from utils.getRoleByName import getRoleByName
from utils.leaderboard.checkName import checkName
from utils.myTypes import Setup
from utils.leaderboard.getPlayerStats import API_RANK, getPlayerStats
from utils.RoleButtons import buttonHandler
import logging

ROLE_LIST = [
    "Unranked",
    "Iron",
    "Bronze",
    "Silver",
    "Gold",
    "Platine",
    "Diamant",
    "Master",
    "Grandmaster",
    "Challenger"
]

_logger = logging.getLogger(__name__)


def getBotRank(rank: int):
    for rank_api, rank_int in API_RANK.items():
        if rank_int == rank:
            return rank_api

async def createNewUserForNewMember(self: Setup, member: Member, channel: TextChannel):
    while True:
        member_message = await self.wait_for("message", check=lambda m: m.author == member)
        message = await channel.send(
            "Je vérifie que ton compte existe bien sur le serveur EUW... (cela peut prendre quelques secondes)"
        )
        summoner_name = member_message.content
        league_id = await checkName(summoner_name)
        if not league_id:
            await message.edit(
                content="Je n'ai pas pu trouver ton nom d'invocateur, merci de le ressaisir et de vérifier que ton compte est bien sur le serveur EUW. Si tu pense que c'est une erreur, merci de contacter <@222008900025581568>."
            )
        else:
            break
    self.db.createUser(member.id)
    tier, rank, lp, summoner_name = await getPlayerStats(self.riot_token, league_id, summoner_name)
    try:
        self.db.addAccountToUser(member.id, summoner_name, tier, rank, lp, league_id)
    except AlreadyExists as e:
        await channel.send(e, "Merci de contacter <@222008900025581568> si il s'agit d'une erreur.")
        await channel.send(
            "Je n'ai pas pu trouver ton nom d'invocateur, merci de le ressaisir et de vérifier que ton compte est bien sur le serveur EUW."
        )
        return createNewUserForNewMember(self, member, channel)
    tier = ROLE_LIST[tier]
    rank = getBotRank(rank)
    msg = f"Tu es actuellement **{tier}"
    if tier != "Unranked":
        msg += f" {rank} {lp}lp"
    msg += "**,\n"
    sended_msg = await channel.send(msg)
    await sended_msg.edit(content=f"{msg}Si ce n'est pas le cas, tu peux contacter <@222008900025581568> pour obtenir de l'aide.")
    await refreshUserRole(await self.fetch_guild(self.guild_id), member, tier)
    return summoner_name

async def onMemberJoin(self: Setup, member: Member):
    tag = member.mention
    new_member_role = getRoleByName(member.guild, "Nouveau")
    await member.add_roles(new_member_role)
    if self.db.checkUserExist(member.id) and not self.is_test_mode:
        await member.remove_roles(new_member_role)
        return
    guild = self.get_guild(self.guild_id)
    await member.create_dm()
    channel = member.dm_channel
    first_message = f"Salut {member.mention}, tout d'abord bienvenue à toi ! <:ZoeAery:856346121102032918>\n"\
        f"Pour commencer, envoie-moi ton nom d'invocateur (ton pseudo sur League). Vérifie bien que tu sois en EUW !\n"
    try:
        await channel.send(first_message)
    except:
        channel = await guild.create_text_channel(f"{member.name}-DM", overwrites={
                member: permissions.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
                guild.default_role: permissions.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False)
            }, reason=f"{member.mention} got closed DM channel", default_auto_archive_duration=1440
        )
        await channel.send(first_message)
    summoner_name = await createNewUserForNewMember(self, member, channel)
    await channel.send("Tu peux maintenant choisir ton main rôle", view=buttonHandler(guild, channel))
    await member.remove_roles(new_member_role)
    _logger.info(f"{member} has been registred as {summoner_name}")
