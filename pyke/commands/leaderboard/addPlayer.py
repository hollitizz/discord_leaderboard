
from discord import Interaction, Member
from utils.SQLRequests import AlreadyExists
from utils.leaderboard.getPlayerStats import getPlayerStats
from utils.myTypes import Setup

from utils.leaderboard.checkName import checkName


async def addPlayer(self: Setup, ctx: Interaction, member: Member, summoner_name: str):
    league_id = await checkName(summoner_name)
    if not league_id:
        await ctx.response.send_message(f"{summoner_name}, ce compte doit être enregistré sur le serveur EUW .\n Vérifie l'orthographe et réessaye !", ephemeral=True)
        return
    if not self.db.checkUserExist(member.id):
        self.db.createUser(member.id)
    tier, rank, lp, summoner_name = await getPlayerStats(self.riot_token, league_id, summoner_name)
    try:
        self.db.addAccountToUser(member.id, summoner_name, tier, rank, lp, league_id)
    except AlreadyExists as e:
        await ctx.response.send_message(e, ephemeral=True)
        return
    await ctx.response.send_message(f"{member.mention} est enregistré, il devrais apparaître dans le leaderboard d'ici 10 minutes !", ephemeral=True)