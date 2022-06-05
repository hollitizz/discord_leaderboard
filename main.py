import dotenv
import os
import inspect
import asyncio

import cogs

from utils.Setup import Setup


dotenv.load_dotenv()
TOKEN = os.getenv('TEST_TOKEN')

async def main():
    bot = Setup(os.getenv('TEST_TOKEN'), os.getenv('RIOT_API_KEY'))
    for cogName, _ in inspect.getmembers(cogs):
        if inspect.isclass(_):
            await bot.load_extension(f"cogs.{cogName}")
    await bot.start(bot.token)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
