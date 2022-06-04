from discord.ext import commands
from discord_slash import cog_ext

def mySlashCommand(name, usage, **attrs):
    return commands.command(name=name, usage=usage, **attrs), cog_ext.cog_slash(name=name, **attrs)