from discord import Member
from utils.myTypes import Setup
import logging


_logger = logging.getLogger(__name__)


async def onMemberRemove(self: Setup, member: Member):
    if self.db.checkUserExist(member.id):
        self.db.deleteUser(member.id)
        logging.info(f"{member} left the server")
