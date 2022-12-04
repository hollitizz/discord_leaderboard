import requests
import urllib
import os

def checkName(summoner_name: str):
    link = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{urllib.parse.quote(summoner_name)}?api_key={os.getenv('RIOT_API_KEY')}"
    r = requests.get(link)
    res = r.json()
    try:
        return res["id"]
    except:
        return None
