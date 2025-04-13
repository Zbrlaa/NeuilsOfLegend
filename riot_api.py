import os
from dotenv import load_dotenv
import httpx
import asyncio

load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
BASE_URL_1 = "https://euw1.api.riotgames.com"
BASE_URL_2 = "https://europe.api.riotgames.com"

headers = {
	"X-Riot-Token": RIOT_API_KEY
}

async def get_account_by_name(gameName: str, tagLine: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_2}/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
		response = await client.get(url, headers=headers)
		response.raise_for_status()
		return response.json()
	
async def get_summoner_by_puuid(puuid: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/summoner/v4/summoners/by-puuid/{puuid}"
		response = await client.get(url, headers=headers)
		response.raise_for_status()
		return response.json()

async def get_league_by_puuid(puuid: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/league/v4/entries/by-puuid/{puuid}"
		response = await client.get(url, headers=headers)
		response.raise_for_status()
		return response.json()

async def get_top_champion_masteries_by_puuid(puuid: str, count: int = 10):
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL_1}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top"
        params = {"count": count}
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

async def get_clash_tournaments():
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL_1}/lol/clash/v1/tournaments"
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

async def get_clash_player_by_puuid(puuid: str):
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL_1}/lol/clash/v1/players/by-puuid/{puuid}"
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

	
puuid = asyncio.run(get_account_by_name("Zbrlaa", "669"))["puuid"]
print(puuid)
summoner = asyncio.run(get_summoner_by_puuid(puuid))
league = asyncio.run(get_league_by_puuid(puuid))
top_mastery = asyncio.run(get_top_champion_masteries_by_puuid(puuid))
tournaments = asyncio.run(get_clash_tournaments())

print(summoner)
print(league[0])
for mastery in top_mastery :
	print(mastery)
for tournament in tournaments :
	print(tournament)