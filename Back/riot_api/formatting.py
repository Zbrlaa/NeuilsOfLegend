# riot_api/formatting.py
from datetime import datetime


def format_timestamp(ms: int) -> str:
    dt = datetime.fromtimestamp(ms / 1000)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_champion(champion: dict) -> dict:
    return {
        "id": champion["key"],
        "name": champion["name"],
        "title": champion["title"]
        # ,"blurb": champion["blurb"]
    }

def format_mastery(mastery: dict, champions: dict) -> dict:
    champion_data = champions.get(str(mastery["championId"])) or {}
    return {
        "champion": champion_data.get("name", "Inconnu"),
        "level": mastery["championLevel"],
        "points": mastery["championPoints"],
        "lastPlayed": format_timestamp(mastery["lastPlayTime"])
    }

def format_clash_tournament(tournament: dict) -> dict:
	return {
		"id": tournament["id"],
		"theme": tournament.get("nameKey", ""),
		"day": tournament.get("nameKeySecondary", ""),
		"schedule": [
			{
				"id": s["id"],
				"registrationTime": format_timestamp(s["registrationTime"]),
				"startTime": format_timestamp(s["startTime"]),
				"cancelled": s["cancelled"]
			} for s in tournament.get("schedule", [])
		]
	}