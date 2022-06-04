from utils.leaderboard.addPlayerOpgg import addPlayerOpgg
from utils.leaderboard.checkOpggLinkIsValid import checkOpggLinkIsValid


async def onMessage(bot, message):
    if message.channel.id in bot.db.opgg_channels\
        and not message.author.bot and checkOpggLinkIsValid(message):
        bot.Db = await addPlayerOpgg(bot.Db, message)
    else:
        await bot.process_commands(message)