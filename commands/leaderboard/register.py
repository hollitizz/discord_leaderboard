from time import sleep
from discord import Interaction

from utils.myTypes import User
from utils.leaderboard.checkName import checkName
from utils.leaderboard.createPlayer import createPlayer
from utils.myTypes import Setup


async def register(self: Setup, ctx: Interaction, summoner_name: str):
    if not summoner_name:
        raise Exception("Tu dois donner ton nom d'invocateur pour t'enregistrer !")
    player_id = checkName(summoner_name)
    if not player_id:
        raise Exception("Ce nom n'est pas valide, ton compte doit être enregistré sur le serveur EUW .\n Vérifie l'orthographe et réessaye !")
    new_user = User(ctx.user.mention, summoner_name, player_id)
    await new_user.setStats(self.riot_token)
    await createPlayer(self, new_user)
    await ctx.response.send_message("Tu es enregistré, tu devrais obtenir tes roles et apparaître dans le leaderboard d'ici 5 minutes !", ephemeral=True)