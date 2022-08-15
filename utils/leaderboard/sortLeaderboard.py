from utils.getChannelByName import getChannelByName
from utils.myTypes import Setup, userList
from discord import Interaction, TextChannel


RANK_EMOJI = [
    "<:ss:934834425705955368>",
    "<:ironS12:934832930675630111>",
    "<:bronzeS12:934832964351717416>",
    "<:silverS12:934832980793389107>",
    "<:goldS12:934832999499964416>",
    "<:platineS12:934833013844500510>",
    "<:diamantS12:934833028943994890>",
    "<:masterS12:934833052641800232>",
    "<:grandmasterS12:934833074754183198>",
    "<:challengerS12:934833092114399242>"
]

def getRanking(i):
    if (i == 1):
        return ":first_place:"
    if (i == 2):
        return ":second_place:"
    if (i == 3):
        return ":third_place:"
    return f" {i}. "

async def resetLeaderboard(self: Setup, channel: TextChannel, newLength: int):
    for msg_id in self.db.leaderboard.msgs:
        try:
            msg = await channel.fetch_message(msg_id)
            await msg.delete()
        except:
            continue
    self.db.leaderboard.msgs.clear()
    for i in range(newLength):
        new_msg = await channel.send("ㅤ")
        self.db.leaderboard.msgs.append(new_msg.id)

async def printLeaderboard(self: Setup):
    msgs: list[list[str]] = [[]]
    msg_len = 0
    msg_nbr = 0
    users: userList = self.db.leaderboard.users

    for i, user in enumerate(users):
        if user.tier == 0 or not user.is_displayed:
            i -= 1
            continue
        else:
            new_line =  (f'{getRanking(i + 1)} '
                        f'{user.tag}, '
                        f'{user.name} est '
                        f'{RANK_EMOJI[user.tier]}'
                        f'{(" " + str(user.rank)) if user.tier < 7 else ""}, '
                        f'{user.lp} LP')
        msg_len += len(new_line)
        if msg_len > 1850:
            msgs.append([])
            msg_nbr += 1
            msg_len = 0
        msgs[msg_nbr].append(new_line)
    channel = getChannelByName(self, "leaderboard")
    if len(msgs) > len(self.db.leaderboard.msgs):
        await resetLeaderboard(self, channel, len(msgs))
    for msg, msg_id in zip(msgs, self.db.leaderboard.msgs):
        try:
            to_edit = await channel.fetch_message(msg_id)
        except:
            await resetLeaderboard(self, channel, len(msgs))
            await printLeaderboard(self)
            return
        try:
            await to_edit.edit(content="\n".join(msg))
        except:
            await to_edit.edit(content="ㅤ")



async def sortLeaderboard(self: Setup):
    users: userList = self.db.leaderboard.users
    i = 0

    while (i < len(users) - 1):
        if (users[i].tier < users[i + 1].tier or
                (users[i].tier == users[i + 1].tier and
                users[i].rank > users[i + 1].rank) or
                    (users[i].tier == users[i + 1].tier and
                    users[i].rank == users[i + 1].rank and
                    users[i].lp < users[i + 1].lp)):
            tmp = users[i]
            users[i] = users[i + 1]
            users[i + 1] = tmp
            i = 0
        else:
            i += 1
    await printLeaderboard(self)
    self.save()
