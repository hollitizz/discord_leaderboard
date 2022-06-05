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
    #TODO: automatic deletion of the user
    return user, user_roles

async def setRole(user: User, role: Role):
    await user.add_roles(role)

async def unsetRole(user: User, role: Role):
    await user.remove_roles(role)

async def refreshRoles(self: Setup):
    users = self.db.leaderboard.users
    guild = self.get_guild(832250335631376455)
    for user in users:
        role_set = False
        discord_user: User = None
        user_roles: list[Role] = []
        try:
            discord_user, user_roles = getUser(guild, user)
        except:
            print(f"{user.tag} is not on this server, please delete him")
            continue
        for role in user_roles:
            if role.name == "mets ton OPGG":
                unsetRole(discord_user, role)
            if role.name in ROLE_LIST and role.name != ROLE_LIST[user.tier]:
                unsetRole(discord_user, role)
            if role.name == ROLE_LIST[user.tier]:
                role_set = True
        if not role_set:
            setRole(discord_user, getRoleByName(guild, ROLE_LIST[user.tier]))