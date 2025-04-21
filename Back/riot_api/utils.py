import httpx
from .config_data import BASE_DDRAGON

async def get_latest_version() -> str:
	url = f"{BASE_DDRAGON}/api/versions.json"
	async with httpx.AsyncClient() as client:
		resp = await client.get(url)
		resp.raise_for_status()
		return resp.json()[0]