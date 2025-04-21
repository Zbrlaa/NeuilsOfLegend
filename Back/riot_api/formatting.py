# riot_api/formatting.py
from datetime import datetime


def format_timestamp(ms: int) -> str:
	dt = datetime.fromtimestamp(ms / 1000)
	return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_champion(champion: dict) -> dict :
	return {
		"id": champion["key"],
		"name": champion["name"],
		"title": champion["title"]
		# ,"blurb": champion["blurb"]
	}

def format_mastery(mastery: dict, champions: dict) -> dict :
	champion_data = champions.get(str(mastery["championId"])) or {}
	return {
		"champion": champion_data.get("name", "Inconnu"),
		"level": mastery["championLevel"],
		"points": mastery["championPoints"],
		"lastPlayed": format_timestamp(mastery["lastPlayTime"])
	}

def format_clash_tournament(tournament: dict) -> dict :
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

def format_match(match: dict) -> dict:
	info = match["info"]
	metadata = match["metadata"]

	return {
		"matchId": metadata["matchId"],
		"gameMode": info.get("gameMode", ""),
		"gameDuration": (info.get("gameStartTimestamp", 0)-info.get("gameEndTimestamp",0)//60000),
		"queueId": info.get("queueId", 0),
		"tournamentCode" : info.get("tournamentCode",""),
		"teams": {
			team["teamId"] : {
				"teamId": team["teamId"],
				"win": team["win"],
				"bans" : team["bans"],
				"objectives" : team["objectives"]
			}
			for team in info.get("teams", [])
		},
		"participants": {
			p["puuid"] : {
				"puuid": p["puuid"],
				"summonerName": p["summonerName"],
				"win": p["win"],
				"teamId": p["teamId"],
				"championId" : p["championId"],
				"championName": p["championName"],
				"kills": p["kills"],
				"deaths": p["deaths"],
				"assists": p["assists"],
				"summoners" : [(p[f"summoner{i}Id"], p[f"summoner{i}Casts"]) for i in range(1,3)],
				"champLevel" : p["champLevel"],
				"totalDamage": p["totalDamageDealtToChampions"],
				"goldEarned" : p["goldEarned"],
				"totalMinionsKilled" : p["totalMinionsKilled"],
				"doubleKills" : p["doubleKills"],
				"tripleKills" : p["tripleKills"],
				"quadraKills" : p["quadraKills"],
				"pentaKills" : p["pentaKills"],
				"items": [p[f"item{i}"] for i in range(7)],
				"spellsCasts" : [p[f"spell{i}Casts"] for i in range(1,5)]
			}
			for p in info.get("participants", [])
		}
	}