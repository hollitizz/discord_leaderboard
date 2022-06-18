from discord import Interaction
from utils.RoleButtons import buttonHandler
from utils.myTypes import Setup

async def changeRole(self: Setup, ctx: Interaction):
    await ctx.response.send_message(
        "Tu peux choisir ton role avec les boutons ci-dessous :",
        view=buttonHandler(ctx.guild),
        ephemeral=True
    )