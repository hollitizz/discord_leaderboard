from discord import Interaction, Member
from utils.myTypes import Setup
import re
import urllib.parse

from logging import getLogger

_logger = getLogger(__name__)

async def getOpgg(self: Setup, ctx: Interaction, req: str, sep:str):
    member_list: list[Member] = []
    for mention in req.split(sep):
        try:
            fetched_member: Member = await ctx.guild.fetch_member(re.sub("[^0-9]", "", mention))
        except:
            continue
        member_list.append(fetched_member)
    msg: list[str] = [f"Voici le{'' if len(member_list) <= 1 else 's' } opgg demandé{'' if len(member_list) <= 1 else 's' } :"]
    multi = "https://euw.op.gg/multisearch/euw?summoners="
    if not member_list:
        raise Exception("Aucune mention valide n'a été trouvé dans ton message")
    opgg_len = 0
    for i, user_tag in enumerate(member_list):
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
    await ctx.response.send_message("\n".join(msg), ephemeral=True)

