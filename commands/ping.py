from discord.ext import commands

async def commandPing(ctx: commands.Context):
    await ctx.reply("Pong !")

async def slashPing(ctx: commands.Context):
    await ctx.reply("Pong !", hidden=True)