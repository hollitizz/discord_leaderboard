import discord
from Bot import Bot

import logging


discord.utils.setup_logging()

if __name__ == "__main__":
    try:
        bot = Bot(is_test_mode=False)
        bot.run(bot.token, reconnect=True, log_handler=None)
    except KeyboardInterrupt:
        logging.warning("\nExiting...")
        bot.session.close()
        bot.db.close()
