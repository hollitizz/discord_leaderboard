import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer, VoiceProtocol
import youtube_dl

class Video:
    def __init__(self):
        self.ytdl = youtube_dl.YoutubeDL({'format': 'bestaudio'})

    def play(self, obj, client: VoiceProtocol, url: str):
        video = self.ytdl.extract_info(url, download=False)
        video_format = video['formats'][0]
        self.stream_url = video_format['url']
        FFMPEG_OPTIONS = {
            "before_options" : "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 0",
            "options": "-vn"
        }
        source = PCMVolumeTransformer(FFmpegPCMAudio(self.stream_url, **FFMPEG_OPTIONS))
        def leave(_):
            asyncio.run_coroutine_threadsafe(client.disconnect(), obj.bot.loop)
        client.play(source, after=leave)