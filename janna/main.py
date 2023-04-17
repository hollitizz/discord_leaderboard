from Bot import Bot
from utils import loggingConfig
import logging

loggingConfig.setupLogging()

if __name__ == "__main__":
    _logger = logging.getLogger("main")
    try:
        bot = Bot(is_test_mode=False)
        bot.run(bot.token, reconnect=True, log_handler=None)
    except KeyboardInterrupt:
        logging.warning("\nExiting...")
        bot.session.close()
        bot.db.close()
