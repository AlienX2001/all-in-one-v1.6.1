from os import path
import httpx
import trio
import re
import json


class HTBot():
    def __init__(self, email, password, api_token=""):
        self.email = email
        self.password = password
        self.api_token = api_token

        self.is_vip = False

        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"
        }
        self.session = httpx.AsyncClient(headers=self.headers, timeout=360.0)
        self.locks = {
                "notif": trio.Lock(),
                "write_users": trio.Lock(),
                "write_boxs": trio.Lock(),
                "write_progress": trio.Lock(),
                "ippsec": trio.Lock(),
                "write_challs": trio.Lock(),
                "refresh_challs": trio.Lock()
                }

        self.payload = {'api_token': self.api_token}
        self.last_checked = []
        self.regexs = {
            "box_pwn": "(?:.*)profile\/(\d+)\">(?:.*)<\/a> owned (.*) on <a(?:.*)profile\/(?:\d+)\">(.*)<\/a> <a(?:.*)",
            "chall_pwn": "(?:.*)profile\/(\d+)\">(?:.*)<\/a> solved challenge <(?:.*)>(.*)<(?:.*)><(?:.*)> from <(?:.*)>(.*)<(?:.*)><(?:.*)",
            "new_box_incoming": "(?:.*)Get ready to spill some (?:.* blood .*! <.*>)(.*)<(?:.* available in <.*>)(.*)<(?:.*)><(?:.*)",
            "new_box_out": "(?:.*)>(.*)<(?:.*) is mass-powering on! (?:.*)",
            "vip_upgrade": "(?:.*)profile\/(\d+)\">(?:.*)<\/a> became a <(?:.*)><(?:.*)><(?:.*)> V.I.P <(?:.*)",
            "writeup_links": "Submitted By: <a href=(?:.*?)>(.*?)<(?:.*?)Url: (?:.*?)href=\"(.*?)\"",
            "check_vip": "(?:.*)Plan\: <span class=\"c-white\">(\w*)<(?:.*)",
            "owns": "owned (challenge|user|root|) <(?:.*?)>(?: |)<(?:.*?)>(?: |)(.*?)(?: |)<",
            "chall": "panel-tools\"> (\d*\/\d*\/\d*) (?:.*?)\"text-(success|warning|danger)\">(?:.*?)(?:\[(\d*?) Points\]|) <\/span> (.*?) \[by <(?:.*?)>(.*?)<\/a>\](?:.*?)\[(\d*?) solvers\](?:.*?)challenge=\"(.*?)\" data-toggle=(?:.*?)Rate Pro\">(\d*?) <(?:.*?)Rate Sucks\">(\d*?) <(?:.*?)> First Blood: <(?:.*?)>(.*?)<(?:.*?)><\/span><br><br>(.*?)<br> <br> (?:<p|<\/div)",
            "chall_diff": "diffchart(\d*)\"\)\.sparkline\((\[.*?\])",
            "chall_status": "<h3>(Active|Retired) \((?:\d*?)\)<\/h3>"
        }
        self.notif = {
            "update_role": {
                "state": False,
                "content": {
                    "discord_id": "",
                    "prev_rank": "",
                    "new_rank": ""
                }
            },
            "new_user": {
                "state": False,
                "content": {
                    "discord_id": "",
                    "level": ""
                }
            },
            "new_box": {
                "state": False,
                "content": {
                    "incoming": False,
                    "box_name": "",
                    "time": ""
                }
            },
            "box_pwn": {
                "state": False,
                "content": {
                    "discord_id": "",
                    "pwn": "",
                    "box_name": "",
                }
            },
            "chall_pwn": {
                "state": False,
                "content": {
                    "discord_id": "",
                    "chall_name": "",
                    "chall_type": ""
                }
            },
            "vip_upgrade": {
                "state": False,
                "content": {
                    "discord_id": ""
                }
            }
        }
        if path.exists("users.txt"):
            with open("users.txt", "r") as f:
                self.users = json.loads(f.read())
        else:
            self.users = []

        if path.exists("boxs.txt"):
            with open("boxs.txt", "r") as f:
                self.boxs = json.loads(f.read())
        else:
            self.boxs = []

        if path.exists("challenges.txt"):
            with open("challenges.txt", "r") as f:
                self.challs = json.loads(f.read())
        else:
            self.challs = []

        if path.exists("progress.txt"):
            with open("progress.txt", "r") as f:
                self.progress = json.loads(f.read())
        else:
            self.progress = []

        if path.exists("resources/ippsec.txt"):
            with open("resources/ippsec.txt", "r") as f:
                self.ippsec_db = json.loads(f.read())
        else:
            self.ippsec_db = []


    async def write_users(self, users):
        async with self.locks["write_users"]:
            self.users = users
            with open("users.txt", "w") as f:
                f.write(json.dumps(users))


    async def write_boxs(self, boxs):
        async with self.locks["write_boxs"]:
            self.boxs = boxs
            with open("boxs.txt", "w") as f:
                f.write(json.dumps(boxs))


    async def write_challs(self, challs):
        async with self.locks["write_challs"]:
            self.challs = challs
            with open("challenges.txt", "w") as f:
                f.write(json.dumps(challs))


    async def write_progress(self, progress):
        async with self.locks["write_progress"]:
            self.progress = progress
            with open("progress.txt", "w") as f:
                f.write(json.dumps(progress))


    async def login(self):
        req = await self.session.get("https://www.hackthebox.eu/login")

        html = req.text
        csrf_token = re.findall(r'type="hidden" name="_token" value="(.+?)"', html)

        if not csrf_token:
            return False

        data = {
            "_token": csrf_token[0],
            "email": self.email,
            "password": self.password
        }

        req = await self.session.post('https://www.hackthebox.eu/login', data=data)

        if req.status_code == 200:
            print("Connecté à HTB !")
            return True

        print("Connexion impossible.")
        return False

    async def verify_user(self, discord_id, htb_acc_id):
        req = await self.session.get("https://www.hackthebox.eu/api/users/identifier/" + htb_acc_id, headers=self.headers)

        if req.status_code == 200:
            users = self.users

            user_info = json.loads(req.text)

            for user in users:
                if user["discord_id"] == discord_id:
                    return "already_in"

            users.append({
                "discord_id": discord_id,
                "htb_id": user_info["user_id"],
            })
            await self.write_users(users)
            return "accepted"

        else:
            return "wrong_id"


    def discord_htb_converter(self, id, discord_to_htb=False, htb_to_discord=False):
        users = self.users

        if discord_to_htb:
            for user in users:
                if user["discord_id"] == id:
                    return user["htb_id"]
            return False

        elif htb_to_discord:
            for user in users:
                if user["htb_id"] == id:
                    return user["discord_id"]
            return False

    def leaderboard(self):
        if path.exists("users.txt"):
            with open("users.txt", "r") as f:
                users = json.loads(f.read())
        else:
            users = []
            return False

        board = sorted(users, key = lambda i: int(i['points']),reverse=True)
        if len(board) > 15:
            board = board[:15]

        return board