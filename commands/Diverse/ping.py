from discord_slash import SlashContext

async def ping(ctx: SlashContext):
    await ctx.send("Pong !", hidden=True)