from discord_slash import SlashContext

from utils.Setup import Setup

async def refresh(ctx: SlashContext, bot: Setup):
    msg = await ctx.send("Refreshing Stats...", hidden=True)
    # refreshStats(ctx, bot)
    await msg.edit("Sorting Leaderboard...", hidden=True)
    # sortLeaderboard(ctx, bot)
    await msg.edit("Refresing Roles...", hidden=True)
    # refreshRoles(ctx, bot)
    await msg.edit("Refresh Done !", hidden=True)