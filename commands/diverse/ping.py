from time import sleep
from discord import Interaction

async def ping(ctx: Interaction):
    await ctx.response.send_message("Pong !", ephemeral=True)
    # sleep(1)
    # await ctx.response.edit_message()
