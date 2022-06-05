from time import sleep
from discord import Interaction
from utils.myTypes import Setup

async def register(self: Setup, ctx: Interaction):
    await ctx.response.send_message("Registering...", ephemeral=True)
    # await self.db.register(ctx.author)
    sleep(1)
    await ctx.response.send_message("Done !", ephemeral=True)