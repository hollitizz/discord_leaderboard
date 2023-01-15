from discord import Interaction, Member
from utils.myTypes import Setup
import re
import urllib.parse

from logging import getLogger

_logger = getLogger(__name__)

def _getMultipleOpgg(self: Setup, ctx: Interaction, users: 'list[Member]'):
    opgg_len = 0
    multi = "https://euw.op.gg/multisearch/euw?summoners="
    msg: list[str] = [f"Voici le{'' if len(users) <= 1 else 's' } opgg demandé{'' if len(users) <= 1 else 's' } :"]
    for i, user_tag in enumerate(users):
        summoner_name = None
        try:
            summoner_name = self.db.getLeagueMainAccountNameFromUserId(user_tag.id)
        except Exception as e:
            _logger.error(e)
        if summoner_name is None:
            msg.append(f"{user_tag.mention} semble ne pas avoir mis son opgg !")
        else:
            msg.append(f"{user_tag.mention} : https://euw.op.gg/summoners/euw/{urllib.parse.quote(summoner_name)}")
            multi += urllib.parse.quote(summoner_name) + ','
            opgg_len += 1
    if opgg_len > 1:
        multi = multi[:-1]
        msg.append(f"multi opgg : {multi}")
    return msg

def _getAllUserAccountsOpgg(self: Setup, ctx: Interaction, user: Member):
    accounts = self.db.getUserAccountsLeagueId(user.id)
    if not accounts:
        msg = [f"{user.mention} semble ne pas avoir mis son opgg !"]
        return msg
    msg: list[str] = [f"Voici l{'\'' if len(accounts) == 1 else 'es' } opgg de {user.mention} :"]
    multi = "https://euw.op.gg/multisearch/euw?summoners="
    for summoner_name, _ in accounts:
        msg.append(f"https://euw.op.gg/summoners/euw/{urllib.parse.quote(summoner_name)}")
        multi += urllib.parse.quote(summoner_name) + ','
    if len(accounts) > 1:
        multi = multi[:-1]
        msg.append(f"multi opgg : {multi}")
    return msg

async def getOpgg(self: Setup, ctx: Interaction, req: str, sep:str):
    member_list: list[Member] = []
    for mention in req.split(sep):
        try:
            fetched_member: Member = await ctx.guild.fetch_member(re.sub("[^0-9]", "", mention))
        except:
            continue
        member_list.append(fetched_member)
    if not member_list:
        raise Exception("Aucune mention valide n'a été trouvé dans ton message")
    if len(member_list) == 1:
        msg = _getAllUserAccountsOpgg(self, ctx, member_list[0])
    else:
        msg = _getMultipleOpgg(self, ctx, member_list)
    await ctx.response.send_message("\n".join(msg), ephemeral=True)

