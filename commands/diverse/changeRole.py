from discord import Interaction
import discord
from utils.getRoleByName import getRoleByName
from utils.types import Setup

LABELS = ["Top", "Jungle", "Mid", "ADC", "Support", "Cancel"]

class ChangeRoleButton(discord.ui.Button):
    def __init__(self, bot, label):
        super().__init__(style=discord.ButtonStyle.red if label == "Cancel" else discord.ButtonStyle.primary, label=label)
        self.bot = bot
        self.label = label

    async def callback(self, ctx: Interaction):
        member = ctx.user
        if self.label == "Cancel":
            await ctx.response.edit_message(content="La commande est annulée !", view=None)
            return
        for role in member.roles:
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and self.label != role.name:
                await member.remove_roles(role)
        if self.label not in member.roles:
            await member.add_roles(getRoleByName(ctx.guild, self.label))
        await ctx.response.edit_message(content=f"Le role {self.label} vient de t'être attribuer !", view=None)


class ChangeRoleView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        for label in LABELS:
            self.add_item(ChangeRoleButton(bot, label=label))


async def changeRole(self: Setup, ctx: Interaction):
    await ctx.response.defer(ephemeral=True)
    await ctx.edit_original_message(
        content="Tu peux choisir ton role avec les boutons ci-dessous :",
        view=ChangeRoleView(self))