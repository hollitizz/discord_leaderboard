from utils.myTypes import Setup, userList
from discord import Interaction

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
    return " {i}. "

async def printLeaderboard(self: Setup):
    msg = [[]]
    msg_len = 0
    msg_nbr = 0
    users: userList = self.db.leaderboard.users

    for i, user in enumerate(users):
        if user[2] == 0:
            continue
        else:
            new_line =  (f'{getRanking(i + 1)} '
                        f'{user[0]}, '
                        f'{user[1]} est '
                        f'{RANK_EMOJI[user[2]]}'
                        f'{(" " + str(user[3])) if user[2] < 7 else ""}, '
                        f'{user[4]} LP')
        msg_len += len(new_line)
        if msg_len > 1850:
            msg.append([])
            msg_nbr += 1
            msg_len = 0
        msg[msg_nbr].append(new_line)
    channel = await self.fetch_channel(self.channel)
    for chan_id in self.msgs:
        to_edit = await channel.fetch_message(chan_id)
        if msg:
            await to_edit.edit(content="\n".join(msg.pop(0)))
        else:
            await to_edit.edit(content="ㅤ")
    while msg:
        new_msg = await channel.send("\n".join(msg.pop(0)))
        self.msgs.append(new_msg.id)

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
    self.save()