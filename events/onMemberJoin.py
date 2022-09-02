from discord import Member, TextChannel, permissions
from utils.leaderboard.checkIdExist import checkIdExist
from utils.leaderboard.checkName import checkName
from utils.leaderboard.createPlayer import createPlayer
from utils.myTypes import Setup, User
from utils.leaderboard.getPlayerStats import API_RANK
from utils.leaderboard.refreshRoles import ROLE_LIST, getRoleByName
from utils.RoleButtons import buttonHandler

def getBotRank(rank: int):
    for rank_api, rank_int in API_RANK.items():
        if rank_int == rank:
            return rank_api

async def askNewMember(self: Setup, member: Member, channel: TextChannel):
    tag = member.mention
    while True:
        member_message = await self.wait_for("message", check=lambda m: m.author == member)
        summoner_name = member_message.content
        summoner_id = checkName(summoner_name)
        if not summoner_id:
            await channel.send("Je n'ai pas pu trouver ton nom d'invocateur, merci de le ressaisir")
        else:
            break
    new_user = User(tag, summoner_name, summoner_id)
    await new_user.setStats(self.riot_token)
    tier = ROLE_LIST[new_user.tier]
    rank = getBotRank(new_user.rank)
    msg = f"Tu es actuellement **{tier}"
    if tier != "Unranked":
        msg += f" {rank} {new_user.lp}lp"
    msg += "**,\n"
    sended_msg = await channel.send(msg)
    await sended_msg.edit(content=f"{msg}Si ce n'est pas le cas, tu peux contacter <@222008900025581568> pour obtenir de l'aide.")
    return new_user


async def onMemberJoin(self: Setup, member: Member):
    tag = member.mention
    new_member_role = getRoleByName(member.guild, "Nouveau")
    await member.add_roles(new_member_role)
    pos = checkIdExist(self.db.leaderboard.users, tag)
    if pos != -1 and not self.is_test_mode:
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
            }, reason=f"{member.mention} got closed DM channel", default_auto_archive_duration=60
        )
        await channel.send(first_message)
    new_user = await askNewMember(self, member, channel)
    await channel.send("Tu peux maintenant choisir ton main rôle", view=buttonHandler(guild, channel))
    await createPlayer(self, new_user)
    await member.remove_roles(new_member_role)
    print(f"{member} has been registred as {new_user.name}")
