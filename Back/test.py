#riot_api/test.py
import asyncio
from riot_api.riot_api import *
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np


account = asyncio.run(get_account_by_name("jeebzi", "033"))
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
m = asyncio.run(get_match_detail(matchs[0]))
print(m)
m_timeline = asyncio.run(get_match_timeline(matchs[0]))
# print(m_timeline)

position = [frame["participantFrames"]["2"]["position"] for frame in m_timeline["info"]["frames"]]
print(position)
print(mastery_score)
x = [p["x"] for p in position]
y = [p["y"] for p in position]

# Création des segments de ligne [(x0, y0)->(x1, y1), ...]
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Valeur de progression de 0 à 1
progress = np.linspace(0, 1, len(segments))

# Dégradé de couleur du bleu au rouge
lc = LineCollection(segments, cmap="coolwarm", array=progress, linewidth=2)

fig, ax = plt.subplots(figsize=(8, 6))
ax.add_collection(lc)
ax.autoscale()
ax.set_aspect('equal', 'box')
ax.set_title("Trajectoire (bleu → rouge)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.grid(True)
plt.savefig("plot.png")
plt.close()