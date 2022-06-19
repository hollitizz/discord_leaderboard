from discord import Guild, User, Role

from utils.myTypes import Setup

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

def getRoleByName(guild: Guild, role_name: str):
    for role in guild.roles:
        if role.name == role_name:
            return role
    return None

async def getUser(guild: Guild, tag: str):
    tmp = [int(s) for s in tag if s.isdigit()]
    res = ''.join(map(str, tmp))
    user: User = await guild.fetch_member(res)
    user_roles = user.roles
    return user, user_roles

async def setRole(user: User, role: Role):
    await user.add_roles(role)

async def unsetRole(user: User, role: Role):
    await user.remove_roles(role)

async def refreshUserRole(guild: Guild, user):
    role_set = False
    discord_user: User = None
    user_roles: list[Role] = []
    try:
        discord_user, user_roles = await getUser(guild, user.tag)
    except:
        raise Exception(f"{user.tag} is not on this server, please delete him")
    for role in user_roles:
        if role.name == "mets ton OPGG":
            await unsetRole(discord_user, role)
        if role.name in ROLE_LIST and role.name != ROLE_LIST[user.tier]:
            await unsetRole(discord_user, role)
        if role.name == ROLE_LIST[user.tier]:
            role_set = True
    if not role_set:
        await setRole(discord_user, getRoleByName(guild, ROLE_LIST[user.tier]))

async def refreshRoles(self: Setup):
    users = self.db.leaderboard.users
    guild = self.get_guild(self.guild_id)
    for user in users:
        try:
            await refreshUserRole(guild, user)
        except Exception as e:
            print(e)
            if not self.is_test_mode:
                users.remove(user)
                self.db.save()