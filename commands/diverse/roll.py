import random
from discord import Interaction

async def roll(self, ctx: Interaction, min: int, max: int):
    result = random.randint(min, max)
    await ctx.response.send_message(f"Le bot a tiré un {result} !")

async def rollInList(self, ctx: Interaction, liste: str, sep:str):
    draw_list = liste.split(sep)
    await ctx.response.send_message(f"Le bot a tiré un {random.choice(draw_list)} !")