from discord import Interaction
from utils.leaderboard.getPlayerStats import getPlayerStats

from utils.leaderboard.checkName import checkName
from utils.myTypes import Setup


async def register(self: Setup, ctx: Interaction, summoner_name: str):
    if not summoner_name:
        raise Exception("Tu dois donner ton nom d'invocateur pour t'enregistrer !")
    league_id = checkName(summoner_name)
    if not league_id:
        raise Exception("Ce nom n'est pas valide, ton compte doit être enregistré sur le serveur EUW .\n Vérifie l'orthographe et réessaye !")
    if not self.db.checkUserExist(ctx.user.id):
        self.db.createUser(ctx.user.id)
    tier, rank, lp, summoner_name = await getPlayerStats(self.riot_token, league_id)
    self.db.addAccountToUser(ctx.user.id, summoner_name, tier, rank, lp, league_id)
    await ctx.response.send_message("Tu es enregistré, tu devrais apparaître dans le leaderboard d'ici 10 minutes !", ephemeral=True)
