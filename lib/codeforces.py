import requests
from os import path
import json

URL = " https://codeforces.com/api/user.info"

if path.exists("users.txt"):
    with open("users.txt", "r") as f:
        users = json.loads(f.read())
else:
    users = []


def verify_user(discord_id, handle):
    PARAM={'handles':handle}
    r=requests.get(url=URL,params=PARAM)
    data=r.json()
    if(data['status']=="OK"):
        for user in users:
            if(user["discord_id"]==discord_id):
                return "already_in"
            users.append({
                "discord_id": discord_id,
                "id": handle,
            })
            with open("users.txt", "w") as f:
                f.write(json.dumps(users))
            return "accepted"
    else:
        return "wrong_id"