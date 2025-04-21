# riot_api/assets.py
import json
import httpx
from .config_data import BASE_DDRAGON
from .formatting import format_champion


def read_json(path: str) :
	return json.load(open(path, "r"))

async def update_champions_json(version: str, path_champions: str = "data/champions.json") :
	url = f"{BASE_DDRAGON}/cdn/{version}/data/fr_FR/champion.json"
	async with httpx.AsyncClient() as client:
		resp = await client.get(url)
		resp.raise_for_status()
		champions =  resp.json()
		
		champions_formated = {c["key"]: format_champion(c) for c in champions["data"].values()}
		with open(path_champions, "w", encoding="utf-8") as f:
			json.dump(champions_formated, f, indent=4, ensure_ascii=False)

async def update_maps_json(path_maps: str ="data/maps.json") :
	maps = read_json(path_maps)	
	maps_formated = {m["mapId"]: m for m in maps}

	with open(path_maps, "w", encoding="utf-8") as f:
		json.dump(maps_formated, f, indent=4, ensure_ascii=False)

async def update_queues_json(path_queues: str ="data/queues.json") :
	queues = read_json(path_queues)	
	queues_formated = {q["queueId"]: q for q in queues}

	with open(path_queues, "w", encoding="utf-8") as f:
		json.dump(queues_formated, f, indent=4, ensure_ascii=False)