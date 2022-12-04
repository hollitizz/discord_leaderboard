from discord import Member
from utils.leaderboard.checkIdExist import checkIdExist
from utils.myTypes import Setup
import logging


_logger = logging.getLogger(__name__)


async def onMemberRemove(self: Setup, member: Member):
    tag = member.mention
    pos = checkIdExist(self.db.leaderboard.users, tag)
    if (pos == -1):
        return
    logging.info(f"{self.db.leaderboard.users.pop(pos).name} Poped !: Reason: {member} left the server")
    self.save()