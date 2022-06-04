import discord
from discord.ext import commands
from discord_slash import SlashCommand
import dotenv
import os

from cogs.Diverse import Diverse
from cogs.Leaderboard import Leaderboard

from events.onReactionAdd import onReactionAdd
from events.onReactionRemove import onReactionRemove
from events.onMemberRemove import onMemberRemove
from events.onMessage import onMessage
from events.onReady import onReady

import utils.Help as Help
from utils.Db import Db



dotenv.load_dotenv()
TOKEN = os.getenv('TEST_TOKEN')
intents = discord.Intents.all()


class Setup(commands.Bot):
    def __init__(self):
        super().__init__("!", intents=intents, help_command=Help.EmbeddedHelpCommand(
                color=0x4c030d, dm_help=True, sort_command=True,
                author_tag="Hollitizz#0111", author_id=222008900025581568,
                author_pp_link="https://cdn.discordapp.com/avatars/222008900025581568/751fdd80170da1a0e368a812faa840a2.webp?size=1024"
            )
        )
        self.Db = Db()
        self.db = self.Db.db

    async def on_reaction_add(self, reaction, user):
        self = await onReactionAdd(self, reaction, user)

    async def on_reaction_remove(self, reaction, user):
        self = await onReactionRemove(self, reaction, user)

    async def on_member_remove(self, member):
        self = await onMemberRemove(self, member)

    async def on_message(self, message):
        self = await onMessage(self, message)

    async def on_ready(self):
        self = await onReady(self)



bot = Setup()
slash = SlashCommand(bot, sync_commands=True)
bot.add_cog(Leaderboard(bot))
bot.add_cog(Diverse(bot))
bot.run(TOKEN)