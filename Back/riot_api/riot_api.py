#riot_api/riot_api.py
import httpx
from .formatting import format_clash_tournament, format_mastery
from .config_data import BASE_URL_1, BASE_URL_2, HEADERS
from .config import CHAMPIONS

async def get_account_by_name(game_name: str, tag_line: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_2}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
		response = await client.get(url, headers=HEADERS)
		response.raise_for_status()
		return response.json()
	
async def get_summoner_by_puuid(puuid: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/summoner/v4/summoners/by-puuid/{puuid}"
		response = await client.get(url, headers=HEADERS)
		response.raise_for_status()
		return response.json()

async def get_league_by_puuid(puuid: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/league/v4/entries/by-puuid/{puuid}"
		response = await client.get(url, headers=HEADERS)
		response.raise_for_status()
		return response.json()

async def get_top_champion_masteries_by_puuid(puuid: str, count: int = 10):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top"
		params = {"count": count}
		response = await client.get(url, headers=HEADERS, params=params)
		response.raise_for_status()
		masteries = response.json()
		masteries_formated = [format_mastery(mastery, CHAMPIONS) for mastery in masteries]
		return masteries_formated

async def get_clash_tournaments():
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/clash/v1/tournaments"
		response = await client.get(url, headers=HEADERS)
		response.raise_for_status()
		tournaments = response.json()
		tournaments_formated = [format_clash_tournament(tournament) for tournament in tournaments]
		return tournaments_formated

async def get_clash_player_by_puuid(puuid: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/clash/v1/players/by-puuid/{puuid}"
		response = await client.get(url, headers=HEADERS)
		response.raise_for_status()
		return response.json()

async def get_challenges_by_puuid(puuid: str):
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_1}/lol/challenges/v1/player-data/{puuid}"
		response = await client.get(url, headers=HEADERS)
		response.raise_for_status()
		return response.json()

async def get_matchs_by_queue(puuid: str, queue_id: int = None, start: int = 0, count: int = 5) -> dict:
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_2}/lol/match/v5/matches/by-puuid/{puuid}/ids"
		params = {
			"start": start,
			"count": count,
			**({"queue": q} if (q := queue_id) is not None else {})
		}

		response = await client.get(url, headers=HEADERS, params=params)
		response.raise_for_status()
		return response.json()

async def get_match_detail(match_id: str) -> dict:
	async with httpx.AsyncClient() as client:
		url = f"{BASE_URL_2}/lol/match/v5/matches/{match_id}"
		response = await client.get(url, headers=HEADERS)
		response.raise_for_status()
		return response.json()