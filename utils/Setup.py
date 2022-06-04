import discord
from discord.ext import commands
from DbHandler import DbHandler

from events.onReactionAdd import onReactionAdd
from events.onReactionRemove import onReactionRemove
from events.onMemberRemove import onMemberRemove
from events.onMessage import onMessage
from events.onReady import onReady

class Setup(commands.Bot, DbHandler):
    def __init__(self, token, riot_token):
        super().__init__("!", intents=discord.Intents.all())
        self.token = token
        self.riot_token = riot_token

    async def on_reaction_add(self, reaction, user):
        await onReactionAdd(self, reaction, user)

    async def on_reaction_remove(self, reaction, user):
        await onReactionRemove(self, reaction, user)

    async def on_member_remove(self, member):
        await onMemberRemove(self, member)

    async def on_message(self, message):
        await onMessage(self, message)

    async def on_ready(self):
        await onReady(self)