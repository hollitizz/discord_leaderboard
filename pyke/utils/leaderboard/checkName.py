from asyncio import sleep
import requests
import urllib
import os
import logging

_logger = logging.getLogger(__name__)

async def checkName(summoner_name: str):
    link = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{urllib.parse.quote(summoner_name)}?api_key={os.getenv('RIOT_API_KEY')}"
    r = requests.get(link)
    res = r.json()
    try:
        return res["id"]
    except:
        _logger.error(f"Error while checking summoner name: {res}")
        if res["status"]["status_code"] == 429:
            await sleep(5)
            return (await checkName(summoner_name))
        else:
            return None
