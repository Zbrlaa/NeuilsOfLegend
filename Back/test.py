#riot_api/test.py
import asyncio
from riot_api.riot_api import *


account = asyncio.run(get_account_by_name("Zbrlaa", "669"))
puuid = account["puuid"]
summoner = asyncio.run(get_summoner_by_puuid(puuid))
league = asyncio.run(get_league_by_puuid(puuid))
top_mastery = asyncio.run(get_top_champion_masteries_by_puuid(puuid))
tournaments = asyncio.run(get_clash_tournaments())
challenges = asyncio.run(get_challenges_by_puuid(puuid))
matchs = asyncio.run(get_matchs_by_queue(puuid))
mastery_score = asyncio.run(get_mastery_score(puuid))

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
for match in matchs[:1] :
	m = asyncio.run(get_match_detail(match))
	print(m)
print(mastery_score)