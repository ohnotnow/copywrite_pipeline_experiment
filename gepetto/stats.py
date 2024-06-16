import json
import logging

stats_file = "stats.json"

def update(userid, username, tokens, cost):
    logger = logging.getLogger("discord")
    logger.info(f"Updating stats for user {username} with {tokens} tokens and {cost} cost")
    try:
        with open(stats_file, 'r') as f:
            users = json.load(f)
    except:
        users = {}
    if userid not in users:
        users[userid] = {"username": username, "tokens": tokens, "cost": cost}
    else:
        users[userid]["tokens"] += tokens
        users[userid]["cost"] += cost
        users[userid]["username"] = username
    with open(stats_file, 'w') as f:
        json.dump(users, f)

def get_stats():
    try:
        with open(stats_file, 'r') as f:
            users = json.load(f)
    except:
        users = {}
    return users
