from discord import Guild


def getRoleByName(guild: Guild, role_name: str):
    for role in guild.roles:
        if role.name == role_name:
            return role
    return None
