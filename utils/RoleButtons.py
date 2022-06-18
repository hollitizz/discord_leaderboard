import discord

from utils.leaderboard.refreshRoles import getRoleByName
from utils.myTypes import Setup
from utils.leaderboard.refreshRoles import ROLE_LIST

class buttonHandler(discord.ui.View):

    def __init__(self, guild: discord.Guild):
        super().__init__()
        self.score = 0
        self.lives = 3
        self.userAns = None
        self.currentAns = None
        self.guild = guild

    @discord.ui.button(label="Top", style=discord.ButtonStyle.primary)
    async def buttonTop(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            print(role.name)
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"le role {button.label} t'a été attribué. Tu peux toujours le rechoisir avec /change_role", view=None
        )

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.primary)
    async def buttonJungle(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            print(role.name)
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"le role {button.label} t'a été attribué. Tu peux toujours le rechoisir avec /change_role", view=None
        )

    @discord.ui.button(label="Mid", style=discord.ButtonStyle.primary)
    async def buttonMid(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            print(role.name)
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"le role {button.label} t'a été attribué. Tu peux toujours le rechoisir avec /change_role", view=None
        )

    @discord.ui.button(label="ADC", style=discord.ButtonStyle.primary)
    async def buttonADC(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            print(role.name)
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"le role {button.label} t'a été attribué. Tu peux toujours le rechoisir avec /change_role", view=None
        )

    @discord.ui.button(label="Support", style=discord.ButtonStyle.primary)
    async def buttonSupport(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            print(role.name)
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"le role {button.label} t'a été attribué. Tu peux toujours le rechoisir avec /change_role", view=None
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def buttonCancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content=f"Aucun rôle ne t'a été attribué. Tu peux toujours le rechoisir avec /change_role", view=None
        )
