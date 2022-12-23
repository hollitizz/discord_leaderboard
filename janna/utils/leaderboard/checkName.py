from asyncio import sleep
import requests
import urllib
import os

async def checkName(summoner_name: str):
    link = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{urllib.parse.quote(summoner_name)}?api_key={os.getenv('RIOT_API_KEY')}"
    r = requests.get(link)
    res = r.json()
    try:
        return res["id"]
    except:
        if res["status"]["status_code"] == 404:
            return None
        else:
            await sleep(1)
            return (await checkName(summoner_name))
