# riot_api/champion.py
import httpx
import json
from .config import BASE_DDRAGON
from .formatting import format_champion

async def get_latest_version() -> str:
	async with httpx.AsyncClient() as client:
		url = f"{BASE_DDRAGON}/api/versions.json"
		resp = await client.get(url)
		resp.raise_for_status()
		return resp.json()[0]

async def update_champion_json(version: str):
	url = f"{BASE_DDRAGON}/cdn/{version}/data/fr_FR/champion.json"
	async with httpx.AsyncClient() as client:
		resp = await client.get(url)
		resp.raise_for_status()
		champions = resp.json()["data"]
		formatted = {c["key"]: format_champion(c) for c in champions.values()}
		with open("data/champions.json", "w", encoding="utf-8") as f:
			json.dump(formatted, f, indent=4, ensure_ascii=False)

def load_champions(path: str = "data/champions.json"):
	with open(path, "r", encoding="utf-8") as f:
		return json.load(f)