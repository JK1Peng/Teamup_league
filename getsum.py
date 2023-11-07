import cassiopeia as cass

# 设置你的 Riot API 密钥
cass.set_riot_api_key("RGAPI-ce6b71b7-2dd3-4ec7-adda-92318290d082")  # 这里填写你的 API 密钥

olouqaq = cass.get_summoner(name="olouqaq", region="NA")

print(olouqaq.level)
ranked_queues = olouqaq.league_entries

# 遍历 ranked_queues 并筛选 RANKED_SOLO_5x5
for queue in ranked_queues:
    if queue.queue.value == "RANKED_SOLO_5x5":
        print(f"{queue.tier} {queue.division}, LP: {queue.league_points}")
