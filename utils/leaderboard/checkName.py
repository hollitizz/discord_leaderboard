import requests
import urllib
import os

async def checkName(user):
    link = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{urllib.parse.quote(user)}?api_key={os.getenv('RIOT_API_KEY')}"
    r = requests.get(link)
    res = r.json()
    try:
        return True, res["id"]
    except:
        return False
