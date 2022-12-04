from discord import Interaction, VoiceChannel, VoiceProtocol

from utils.Video import Video


async def player(self, ctx: Interaction, channel: str = None, link: str = None):
    vchannel: VoiceChannel = None
    if not channel:
        try:
            vchannel = ctx.user.voice.channel
        except:
            await ctx.response.send_message("Vous n'êtes pas dans un channel vocal", ephemeral=True)
            return
        for chan in ctx.guild.voice_channels:
            if chan.id == channel:
                vchannel = chan
                break
    if not vchannel:
        await ctx.response.send_message("ce channel n'existe pas", ephemeral=True)
        return
    client: VoiceProtocol = ctx.guild.voice_client
    if not client:
        await vchannel.connect()
    else:
        if channel != client.channel:
            await ctx.response.send_message("Le bot est deja utilisé dans un autre channel.", ephemeral=True)
            return
    client: VoiceProtocol = ctx.guild.voice_client
    video = Video()
    video.play(self, client, link)
    await ctx.response.send_message(f"playing: {link}", ephemeral=True)
