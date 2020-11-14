import requests
from os import path
import json

URL = "https://tryhackme.com/tokens/discord/"

if path.exists("users.txt"):
    with open("users.txt", "r") as f:
        users = json.loads(f.read())
else:
    users = []
    
def verify_user(discord_id,token):
    re = requests.get(URL+token)
    info = re.json()
    if(info['success']==True):
      for user in users:
            if(user["discord_id"]==discord_id):
                return "already_in"
            users.append({
                "discord_id": discord_id,
                "id": info['username'],
            })
            with open("users.txt", "w") as f:
                f.write(json.dumps(users))
            return "accepted"
    else:
      return "wrong_id"
