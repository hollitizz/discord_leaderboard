import asyncio
from utils.myTypes import Setup, userList, User
import requests


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


async def getSummonerDatas(riot_token: str, user: User):
    link = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{user.id}?api_key={riot_token}"
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


async def getPlayerStats(riot_token: str, user: User):
    data = await getSummonerDatas(riot_token, user)
    if (isinstance(data, list)):
        for d in data:
            if d['queueType'] ==  "RANKED_SOLO_5x5":
                filtered_data = d
        if not filtered_data:
            user.name = filtered_data["summonerName"]
            raise
    user.tier = getApiTier(filtered_data["tier"])
    user.rank = getApiRank(filtered_data["rank"])
    user.lp = filtered_data["leaguePoints"]
    return user


async def refreshStats(self: Setup):
    users: userList = self.db.leaderboard.users


    for i, user in enumerate(users):
        if ((i + 1) % 10 == 0):
            await asyncio.sleep(1)
        try:
            user = await getPlayerStats(self.riot_token, user)
        except:
            continue
    self.save()