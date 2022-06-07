from time import sleep
from discord import Interaction

from utils.myTypes import User
from utils.leaderboard.checkName import checkName
from utils.leaderboard.createPlayer import createPlayer
from utils.myTypes import Setup

async def register(self: Setup, ctx: Interaction, summoner_name: str = None):
    if not summoner_name:
        raise Exception("Tu dois donner ton nom d'invocateur pour t'enregistrer !")
    player_id = await checkName(summoner_name)
    print("test")
    if not player_id:
        raise Exception("Ce nom n'est pas valide, ton compte doit être enregistré sur le serveur EUW .\n Vérifie l'orthographe et réessaye !")
    print("test1")
    new_user = User(ctx.user.mention, summoner_name, player_id)
    print("test2")
    await new_user.setStats(self.riot_token)
    print("test3")
    await createPlayer(self, new_user)
    print("test4")
    await ctx.response.send_message("Tu es enregistré, tu devrais obtenir tes roles et apparaître dans le leaderboard d'ici 5 minutes !", ephemeral=True)