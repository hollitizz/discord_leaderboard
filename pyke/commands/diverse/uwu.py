import random
from discord import Interaction
from utils.player import player


async def uwu(self, ctx: Interaction, channel: str = None):
    link = [
        "https://www.youtube.com/watch?v=WLsgxKQLRrYa",
        "https://www.youtube.com/watch?v=4zHrnU9DdDY",
    ]
    await player(self, ctx, channel, random.choice(link))
