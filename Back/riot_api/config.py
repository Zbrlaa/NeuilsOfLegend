# riot_api/config.py
import asyncio
from .assets import read_json
from .utils import get_latest_version


VERSION = asyncio.run(get_latest_version())

CHAMPIONS = read_json("data/champions.json")
MAPS = read_json("data/maps.json")
QUEUE = read_json("data/queues.json")