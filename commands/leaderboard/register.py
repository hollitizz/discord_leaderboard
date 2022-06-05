from time import sleep
from discord import Interaction

from utils.myTypes import User
from utils.leaderboard.checkName import checkName
from utils.leaderboard.createPlayer import create_player
from utils.myTypes import Setup

async def register(self: Setup, ctx: Interaction, summoner_name: str = None):
    if not summoner_name:
        ctx.response.send_message("Tu dois donner ton nom d'invocateur pour t'enregistrer !", ephemeral=True)
        return
    player_id = await checkName(summoner_name)
    if not player_id:
        ctx.response.send_message("Ce nom n'est pas valide, ton compte doit être enregistré sur le serveur EUW .\n Vérifie l'orthographe et réessaye !", ephemeral=True)
        return
    await create_player(self, User(ctx.user.mention, summoner_name,player_id))
    await ctx.response.send_message("Tu es enregistré, tu devrais obtenir tes roles et apparaître dans le leaderboard d'ici 5 minutes !", ephemeral=True)