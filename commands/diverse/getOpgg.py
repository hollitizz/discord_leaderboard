

from discord import Interaction

from utils.leaderboard.checkIdExist import checkIdExist


async def getOpgg(self, ctx: Interaction, req: str, sep: str):
    req_list: list[str] = req.split(sep)
    msg: list[str] = ["Voici le(s) opgg demandé(s):"]
    multi = "https://euw.op.gg/multisearch/euw?summoners="
    for user_tag in req_list:
        pos = checkIdExist(self.bot.db.users, user_tag)
        if pos == -1:
            msg.append(f"{user_tag} semble ne pas avoir mit son opgg !")
        else:
            msg.append(f"{user_tag} : {self.bot.db.users[pos].name}")
            multi += f"{self.bot.db.users[pos].name},"
    if multi != "https://euw.op.gg/multisearch/euw?summoners=":
        msg.append(f"multi opgg : {multi}")
    await ctx.response.send_message("\n".join(msg), ephemeral=True)
