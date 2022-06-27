import random
from discord import Interaction
from utils.player import player


async def uwu(self, ctx: Interaction, channel: str = None):
    link = [
        "https://www.youtube.com/watch?v=WLsgxKQLRrYa",
        "https://www.youtube.com/watch?v=b6LLrr2P0mo"
    ]
    await player(self, ctx, channel, random.choice(link))
