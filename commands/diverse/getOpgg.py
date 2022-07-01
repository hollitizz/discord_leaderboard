from discord import Interaction, Member
from utils.leaderboard.checkIdExist import checkIdExist
import re
import urllib

async def getOpgg(self, ctx: Interaction, req: str, sep: str):
    member_list: list[Member] = []
    for string in req.split(sep):
        try:
            fetched_member: Member = await ctx.guild.fetch_member(re.sub("[^0-9]", "", string))
        except:
            continue
        member_list.append(fetched_member)
    msg: list[str] = ["Voici le(s) opgg demandé(s):"]
    multi = "https://euw.op.gg/multisearch/euw?summoners="
    if not member_list:
        raise Exception("Aucune mention valide n'a été trouvé dans ton message")
    for user_tag in member_list:
        pos = checkIdExist(self.bot.db.leaderboard.users, user_tag.mention)
        if pos == -1:
            msg.append(f"{user_tag.mention} semble ne pas avoir mis son opgg !")
        else:
            msg.append(f"{user_tag.mention} : https://euw.op.gg/summoners/euw/{self.bot.db.leaderboard.users[pos].name}")
            multi += f"{urllib.parse.quote(self.bot.db.leaderboard.users[pos].name)},"
    if len(member_list) > 1:
        msg.append(f"multi opgg : {multi}")
    await ctx.response.send_message("\n".join(msg), ephemeral=True)