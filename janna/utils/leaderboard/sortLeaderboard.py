from utils.getChannelByName import getChannelByName
from utils.myTypes import Setup
from discord import TextChannel
import logging

_logger = logging.getLogger(__name__)

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

def getRanking(i: int):
    if (i == 1):
        return ":first_place:"
    if (i == 2):
        return ":second_place:"
    if (i == 3):
        return ":third_place:"
    return f"{i}. "

async def resetLeaderboard(self: Setup, channel: TextChannel, newLength: int):
    msgs = channel.history(limit=100)
    async for msg in msgs:
        try:
            await msg.delete()
        except:
            continue
    self.db.clearLeaderboardMsgs()
    for i in range(newLength):
        new_msg = await channel.send("ㅤ")
        self.db.addNewLeaderboardMsg(new_msg.id)

def getSortedLeaderboard(self: Setup):
    users = self.db.getSortedUsers()
    msgs: list[list[str]] = [[]]
    msg_len = 0
    msg_nbr = 0

    for i, (user_id, summoner_name, tier, rank, lp) in enumerate(users):
        if tier == 0 or not self.db.checkuserVisibility(user_id):
            continue
        else:
            new_line =  (f'{getRanking(i + 1)} '
                        f'<@{user_id}>, '
                        f'{summoner_name} est '
                        f'{RANK_EMOJI[tier]}'
                        f'{(" " + str(rank)) if tier < 7 else ""}, '
                        f'{lp} LP')
            _logger.info(f'new_line: {new_line}')
        msg_len += len(new_line)
        if msg_len > 1850:
            msgs.append([])
            msg_nbr += 1
            msg_len = 0
        msgs[msg_nbr].append(new_line)
    return msgs

async def printLeaderboard(self: Setup):
    msgs = getSortedLeaderboard(self)
    leaderboard_msgs_id = self.db.getLeaderboardMsgs()
    channel = getChannelByName(self, "leaderboard")
    if len(msgs) > len(leaderboard_msgs_id) or len(msgs) < len(leaderboard_msgs_id):
        _logger.info("Leaderboard not at the good size, reseting")
        await resetLeaderboard(self, channel, len(msgs))
        leaderboard_msgs_id = self.db.getLeaderboardMsgs()
    for msg, msg_id in zip(msgs, leaderboard_msgs_id):
        try:
            to_edit = await channel.fetch_message(msg_id)
        except:
            _logger.info(f"Error while fetching message {msg_id}")
            await resetLeaderboard(self, channel, len(msgs))
            await printLeaderboard(self)
            return
        try:
            await to_edit.edit(content="\n".join(msg))
        except:
            await to_edit.edit(content="ㅤ")
