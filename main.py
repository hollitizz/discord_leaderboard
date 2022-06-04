import dotenv
import os
import inspect

from discord_slash import SlashCommand
import cogs

from utils.Setup import Setup


dotenv.load_dotenv()
TOKEN = os.getenv('TEST_TOKEN')


if __name__ == '__main__':
    bot = Setup(os.getenv('TEST_TOKEN'), os.getenv('RIOT_API_KEY'))
    slash = SlashCommand(bot, sync_commands=True)
    for cogName, _ in inspect.getmembers(cogs):
        if inspect.isclass(_):
            bot.load_extension(f"cogs.{cogName}")
    bot.run(bot.token)