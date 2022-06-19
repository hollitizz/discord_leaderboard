from typing import List
from discord.ext import commands
from discord import Member, app_commands, Interaction, Object

from commands.diverse import ping
from commands.diverse import changeRole
from commands.diverse import roll
from utils.myTypes import Setup


class Diverse(commands.Cog, description="Groupe de commande Divers"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="ping", description="Répond avec \"Pong !\"")
    async def ping(self, ctx: Interaction):
        await ping.ping(ctx)

    @app_commands.command(name="change_role", description="Te permet de changer ton main role")
    async def changeRole(self, ctx: Interaction):
        await changeRole.changeRole(ctx)

    @changeRole.error
    async def changeRoleError(self, ctx: Interaction, error: Exception):
        print(error)
        await ctx.response.send_message(
            f"Une erreur est surevenue, réesaye ou sinon contact un admin",
            ephemeral=True
        )

    @app_commands.command(name="roll", description="Get a random number between two integers")
    @app_commands.describe(min="Minimum roll point, 1 by default", max="Maximum roll point, 6 by default")
    async def roll(self, ctx: Interaction, min: int=1, max: int=6):
        await roll.roll(self, ctx, min, max)

async def setup(bot: Setup):
    await bot.add_cog(Diverse(bot), guilds=[Object(id=bot.guild_id)])