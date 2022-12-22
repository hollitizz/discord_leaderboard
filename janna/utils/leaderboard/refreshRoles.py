from discord import Guild, Member, Role
import logging
from utils.myTypes import Setup, UnknownUser


_logger = logging.getLogger(__name__)


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

async def getUser(guild: Guild, user_id: str):
    user: Member = await guild.fetch_member(user_id)
    user_roles = user.roles
    return user, user_roles


async def refreshUserRole(guild: Guild, user_id, league_tier):
    role_set = False
    discord_user: Member = None
    user_roles: list[Role] = []
    try:
        discord_user, user_roles = await getUser(guild, user_id)
    except:
        raise UnknownUser(f"<@{user_id}>")
    for role in user_roles:
        if role.name == "mets ton OPGG":
            await discord_user.remove_roles(role)
        if role.name in ROLE_LIST and role.name != ROLE_LIST[league_tier]:
            await discord_user.remove_roles(role)
        if role.name == ROLE_LIST[league_tier]:
            role_set = True
    if not role_set:
        await discord_user.add_roles(getRoleByName(guild, ROLE_LIST[league_tier]))


async def refreshRoles(self: Setup):
    users_id = self.db.getUsers()
    guild = self.get_guild(self.guild_id)
    for user_id in users_id:
        try:
            await refreshUserRole(guild, user_id, self.db.getUserMainAccountTier(user_id))
        except UnknownUser as e:
            if not self.is_test_mode:
                self.db.deleteUser(user_id)
                _logger.warning(f"{e} has been deleted from the database cause he's not in the server anymore")
        except Exception as e:
            _logger.error(e)
    self.save()