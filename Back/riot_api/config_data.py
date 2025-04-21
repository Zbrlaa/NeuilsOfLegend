# riot_api/config_data.py
import os
from dotenv import load_dotenv

load_dotenv()


RIOT_API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": RIOT_API_KEY}

BASE_URL_1 = "https://euw1.api.riotgames.com"
BASE_URL_2 = "https://europe.api.riotgames.com"
BASE_DDRAGON = "https://ddragon.leagueoflegends.com"