
from discord import Interaction, Member
from utils.SQLRequests import AlreadyExists
from utils.leaderboard.getPlayerStats import getPlayerStats
from utils.myTypes import Setup
from utils.leaderboard.refreshRoles import refreshUserRole

from utils.leaderboard.checkName import checkName
import logging

_logger = logging.getLogger(__name__)

async def addPlayer(self: Setup, ctx: Interaction, member: Member, summoner_name: str):
    await ctx.response.defer(ephemeral=True, thinking=True)
    league_id = await checkName(summoner_name)
    if not league_id:
        await ctx.edit_original_response(content=f"{summoner_name}, ce compte doit être enregistré sur le serveur EUW .\n Vérifie l'orthographe et réessaye !")
        return
    if not self.db.checkUserExist(member.id):
        self.db.createUser(member.id)
    tier, rank, lp, summoner_name = await getPlayerStats(self.riot_token, league_id, summoner_name)
    try:
        self.db.addAccountToUser(member.id, summoner_name, tier, rank, lp, league_id)
        await refreshUserRole(ctx.guild, member.id, tier)
    except AlreadyExists as e:
        await ctx.edit_original_response(content=f"{e}")
        return
    except Exception as e:
        _logger.exception(e)
        return
    await ctx.edit_original_response(content=f"{member.mention} est enregistré, il devrais apparaître dans le leaderboard d'ici 10 minutes !")