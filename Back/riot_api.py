import os
from dotenv import load_dotenv
import httpx
import asyncio
import json
from datetime import datetime

load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
BASE_URL_1 = "https://euw1.api.riotgames.com"
BASE_URL_2 = "https://europe.api.riotgames.com"
BASE_DDRAGON = "https://ddragon.leagueoflegends.com"

headers = {
	"X-Riot-Token": RIOT_API_KEY
}

def read_json(path: str) :
		return json.load(open(path, "r"))


async def get_latest_version() -> str:
	url = f"{BASE_DDRAGON}/api/versions.json"
	async with httpx.AsyncClient() as client:
		resp = await client.get(url)
		resp.raise_for_status()
		versions = resp.json()
		return versions[0]

VERSION = asyncio.run(get_latest_version())
QUEUES = {q["queueId"]: q for q in read_json("data/queues.json")}

async def update_champion_json(version: str):
	url = f"{BASE_DDRAGON}/cdn/{version}/data/fr_FR/champion.json"
	async with httpx.AsyncClient() as client:
		resp = await client.get(url)
		resp.raise_for_status()
		champions =  resp.json()
		champions_formated = {c["key"]: format_champion(c) for c in champions["data"].values()}
		with open("data/champions.json", "w", encoding="utf-8") as f:
			json.dump(champions_formated, f, indent=4, ensure_ascii=False)

async def update_maps_json():
	maps = read_json("data/maps.json")	
	maps_formated = {m["mapId"]: m for m in maps}

	with open("data/maps.json", "w", encoding="utf-8") as f:
		json.dump(maps_formated, f, indent=4, ensure_ascii=False)

# asyncio.run(update_maps_json())

async def update_queues_json():
	queues = read_json("data/queues.json")	
	queues_formated = {q["queueId"]: q for q in queues}

	with open("data/queues.json", "w", encoding="utf-8") as f:
		json.dump(queues_formated, f, indent=4, ensure_ascii=False)

# asyncio.run(update_queues_json())

# asyncio.run(update_champion_json(VERSION))
CHAMPION = read_json("data/champions.json")
print(CHAMPION)

async def get_account_by_name(game_name: str, tag_line: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_2}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
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
		masteries = response.json()
		masteries_formated = [format_mastery(mastery) for mastery in masteries]
		return masteries_formated

async def get_clash_tournaments():
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/clash/v1/tournaments"
		response = await client.get(url, headers=headers)
		response.raise_for_status()
		tournaments = response.json()
		tournaments_formated = [format_clash_tournament(tournament) for tournament in tournaments]
		return tournaments_formated

async def get_clash_player_by_puuid(puuid: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/clash/v1/players/by-puuid/{puuid}"
		response = await client.get(url, headers=headers)
		response.raise_for_status()
		return response.json()

async def get_challenges_by_puuid(puuid: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/challenges/v1/player-data/{puuid}"
		response = await client.get(url, headers=headers)
		response.raise_for_status()
		return response.json()

async def get_matchs_by_queue(puuid: str, queue_id: int = None, start: int = 0, count: int = 5):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_2}/lol/match/v5/matches/by-puuid/{puuid}/ids"
		params = {
			"start": start,
			"count": count,
			**({"queue": q} if (q := queue_id) is not None else {})
		}

		response = await client.get(url, headers=headers, params=params)
		response.raise_for_status()
		return response.json()

async def get_match_detail(match_id: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_2}/lol/match/v5/matches/{match_id}"
		response = await client.get(url, headers=headers)
		response.raise_for_status()
		return response.json()


print(VERSION)
print(QUEUES.get(450, {}).get("description", "Inconnue"))

account = asyncio.run(get_account_by_name("Zbrlaa", "669"))
puuid = account["puuid"]
summoner = asyncio.run(get_summoner_by_puuid(puuid))
league = asyncio.run(get_league_by_puuid(puuid))
top_mastery = asyncio.run(get_top_champion_masteries_by_puuid(puuid))
tournaments = asyncio.run(get_clash_tournaments())
challenges = asyncio.run(get_challenges_by_puuid(puuid))
matchs = asyncio.run(get_matchs_by_queue(puuid))

print(puuid)
print(account)
print(summoner)
print(league)
for mastery in top_mastery :
	print(mastery)
for tournament in tournaments :
	print(tournament)
# print(challenges)
print(matchs)
# for match in matchs[:1] :
# 	m = asyncio.run(get_match_detail(match))
# 	participant = next(p for p in m["info"]["participants"] if p["puuid"] == puuid) #Info du joueur ciblé
# 	print(participant)
#Durée (gameStartTimestamp-gameEndTimestamp)/60000