from discord import ChannelType, Guild
from discord.ext import commands

def getChannelByName(bot: commands.Bot, name, channelType: ChannelType = ChannelType.text):
    guild: Guild = bot.get_guild(bot.guild_id)
    for channel in guild.channels:
        if name.lower() in channel.name.lower() and channel.type == channelType:
            return channel
    return None