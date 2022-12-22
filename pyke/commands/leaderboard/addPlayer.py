
from discord import Interaction, Member
from utils.leaderboard.getPlayerStats import getPlayerStats
from utils.myTypes import Setup

from utils.leaderboard.checkName import checkName


async def addPlayer(self: Setup, ctx: Interaction, member: Member, summoner_name: str):
    league_id = checkName(summoner_name)
    if not league_id:
        raise Exception(f"{summoner_name}, ce compte doit être enregistré sur le serveur EUW .\n Vérifie l'orthographe et réessaye !")
    if not self.db.checkUserExist(member.id):
        self.db.createUser(member.id)
    tier, rank, lp, summoner_name = await getPlayerStats(self.riot_token, league_id)
    self.db.addAccountToUser(member.id, summoner_name, tier, rank, lp, league_id)
    await ctx.response.send_message(f"{member} est enregistré, il devrais apparaître dans le leaderboard d'ici 5 minutes !", ephemeral=True)