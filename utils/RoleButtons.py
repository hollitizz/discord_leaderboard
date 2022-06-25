import asyncio
import discord
from discord import TextChannel
from discord import DMChannel

from utils.leaderboard.refreshRoles import getRoleByName
from utils.myTypes import WELCOME_MESSAGE

class buttonHandler(discord.ui.View):

    def __init__(self, guild: discord.Guild, channel: TextChannel):
        super().__init__()
        self.score = 0
        self.lives = 3
        self.userAns = None
        self.currentAns = None
        self.guild = guild
        self.channel = channel

    @discord.ui.button(label="Top", style=discord.ButtonStyle.primary)
    async def buttonTop(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"Le rôle {button.label} t'a été attribué. Tu peux toujours le changer à l'aide de la commande **/change_role**.", view=None
        )
        await self.channel.send(WELCOME_MESSAGE)
        if self.channel and not isinstance(self.channel, DMChannel):
            await asyncio.sleep(10)
            await self.channel.delete()

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.primary)
    async def buttonJungle(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"Le rôle {button.label} t'a été attribué. Tu peux toujours le changer à l'aide de la commande **/change_role**.", view=None
        )
        await self.channel.send(WELCOME_MESSAGE)
        if self.channel and not isinstance(self.channel, DMChannel):
            await asyncio.sleep(10)
            await self.channel.delete()

    @discord.ui.button(label="Mid", style=discord.ButtonStyle.primary)
    async def buttonMid(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"Le rôle {button.label} t'a été attribué. Tu peux toujours le changer à l'aide de la commande **/change_role**.", view=None
        )
        await self.channel.send(WELCOME_MESSAGE)
        if self.channel and not isinstance(self.channel, DMChannel):
            await asyncio.sleep(10)
            await self.channel.delete()

    @discord.ui.button(label="ADC", style=discord.ButtonStyle.primary)
    async def buttonADC(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"Le rôle {button.label} t'a été attribué. Tu peux toujours le changer à l'aide de la commande **/change_role**.", view=None
        )
        await self.channel.send(WELCOME_MESSAGE)
        if self.channel and not isinstance(self.channel, DMChannel):
            await asyncio.sleep(10)
            await self.channel.delete()

    @discord.ui.button(label="Support", style=discord.ButtonStyle.primary)
    async def buttonSupport(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(interaction.user.id)
        for role in member.roles:
            if role.name in ["Top", "Jungle", "Mid", "ADC", "Support"] and button.label != role.name:
                await member.remove_roles(role)
        if button.label not in member.roles:
            await member.add_roles(getRoleByName(self.guild, button.label))
        await interaction.response.edit_message(
            content=f"Le rôle {button.label} t'a été attribué. Tu peux toujours le changer à l'aide de la commande **/change_role**.", view=None
        )
        await self.channel.send(WELCOME_MESSAGE)
        if self.channel and not isinstance(self.channel, DMChannel):
            await asyncio.sleep(10)
            await self.channel.delete()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def buttonCancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content=f"Aucun rôle ne t'a été attribué. Tu peux toujours en choisir à l'aide de la commande **/change_role**.", view=None
        )
        await self.channel.send(WELCOME_MESSAGE)
        if self.channel and not isinstance(self.channel, DMChannel):
            await asyncio.sleep(10)
            await self.channel.delete()
