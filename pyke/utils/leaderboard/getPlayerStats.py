from asyncio import sleep
from typing import Tuple
import requests
from logging import getLogger


_logger = getLogger(__name__)


API_TIER = {
    "UNRANKED" : 0,
    "IRON" : 1,
    "BRONZE" : 2,
    "SILVER" : 3,
    "GOLD" : 4,
    "PLATINUM" : 5,
    "DIAMOND" : 6,
    "MASTER" : 7,
    "GRANDMASTER" : 8,
    "CHALLENGER" : 9
}


API_RANK = {
    "0" : 0,
    "I" : 1,
    "II" : 2,
    "III" : 3,
    "IV" : 4
}


async def getSummonerDatas(riot_token: str, league_id):
    link = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{league_id}?api_key={riot_token}"
    r = requests.get(link)
    data = r.json()
    return data


def getApiTier(tier):
    for tier_api, tier_int in API_TIER.items():
        if tier_api == tier:
            return tier_int


def getApiRank(rank):
    for rank_api, rank_int in API_RANK.items():
        if rank_api == rank:
            return rank_int


async def getPlayerStats(riot_token: str, league_id: str, summoner_name: str) -> Tuple[int, int, int, str]:
    data: list[dict] = await getSummonerDatas(riot_token, league_id)
    filtered_data = None
    if (isinstance(data, list)):
        for d in data:
            if d['queueType'] ==  "RANKED_SOLO_5x5":
                filtered_data = d
                summoner_name = d['summonerName']
        if not filtered_data:
            return 0, 1, 0, data[0]['summonerName'] if len(data) > 0 else summoner_name
    else:
        if data['status']['status_code'] == 429:
            _logger.info("Rate limit exceeded, waiting 2 minutes")
            await sleep(120)
            return await getPlayerStats(riot_token, league_id, summoner_name)
        raise Exception(f"Can't Parse Data {data}")
    tier = getApiTier(filtered_data["tier"])
    rank = getApiRank(filtered_data["rank"])
    lp = filtered_data["leaguePoints"]
    return tier, rank, lp, summoner_name
