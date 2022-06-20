
from discord import Interaction, Member

from utils.leaderboard.checkName import checkName
from utils.leaderboard.createPlayer import createPlayer
from utils.myTypes import User


async def addPlayer(self, ctx: Interaction, member: Member, summoner_name: str):
    player_id = checkName(summoner_name)
    if not player_id:
        raise Exception("Ce nom n'est pas valide, le compte doit être enregistré sur le serveur EUW .\n Vérifie l'orthographe et réessaye !")
    new_user = User(member.mention, summoner_name, player_id)
    await new_user.setStats(self.riot_token)
    await createPlayer(self, new_user)
    await ctx.response.send_message(f"{member.name} est maintenant enregistré, tu devrais apparaître dans le leaderboard d'ici 5 minutes !", ephemeral=True)