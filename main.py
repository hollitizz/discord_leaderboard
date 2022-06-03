import discord
from discord.ext import commands
from discord_slash import SlashCommand
import utils.Help as Help
from cogs import Diverse
import dotenv
import os

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()


class Setup(commands.Bot):
    def __init__(self):
        super().__init__("!", intents=intents, help_command=Help.EmbeddedHelpCommand(
                color=0x4c030d, dm_help=True, sort_command=True,
                author_tag="Hollitizz#0111", author_id=222008900025581568,
                author_pp_link="https://cdn.discordapp.com/avatars/222008900025581568/751fdd80170da1a0e368a812faa840a2.webp?size=1024"
            )
        )

    async def on_ready(self):
        print(f"{self.user} is Ready !")


bot = Setup()
slash = SlashCommand(bot, sync_commands=True)
bot.add_cog(Diverse.Diverse(bot))
bot.run(TOKEN)