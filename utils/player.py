from discord import Interaction, VoiceChannel, VoiceProtocol

from utils.Video import Video


async def player(self, ctx: Interaction, channel: str = None, link: str = None):
    if not channel:
        try:
            channel = ctx.user.voice.channel
        except:
            await ctx.response.send_message("Vous n'êtes pas dans un channel vocal", ephemeral=True)
            return
    else:
        channel = self.bot.get_channel(channel)
    if not channel or not isinstance(channel, VoiceChannel):
        await ctx.response.send_message("Vous n'êtes pas dans un channel vocal", ephemeral=True)
        return
    client: VoiceProtocol = ctx.guild.voice_client
    if not client:
        await channel.connect()
    else:
        if channel != client.channel:
            await ctx.response.send_message("Le bot est deja utilisé dans un autre channel.", ephemeral=True)
            return
    client: VoiceProtocol = ctx.guild.voice_client
    video = Video()
    video.play(self, client, link)
