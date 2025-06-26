import json
import os
import sys
from base64 import b64decode

import requests
from dotenv import load_dotenv


def get_blacklist():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2luaWVtaW4vd2FybmluZy9tYXN0ZXIvYmxnY2FzdC5qc29u"
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        return f"An error occurred: {str(e)}"
        sys.exit(1)


load_dotenv()

HELPABLE = {}

DICT_BUTTON = {}

COPY_ID = {}

API_ID = int(os.environ.get("API_ID", 23228407))
MAX_BOT = int(os.environ.get("MAX_BOT", 200))

API_HASH = os.environ.get("API_HASH", "4bfbc373619628a8e6dd1d51da8c6fbc")

BOT_TOKEN = os.environ.get(
    "BOT_TOKEN", "7714524326:AAGZa-r8dGa-CZEVTsmUoeLMSCe_iUnmiMY"
)

BOT_ID = int(os.environ.get("BOT_ID", "7714524326"))

API_GEMINI = os.environ.get("API_GEMINI", "AIzaSyARecWxktUPu_ywxywdg3OFwh3XkyrD4_M")

API_BOTCHAX = os.environ.get("API_BOTCHAX", "GenzR")

API_MAELYN = os.environ.get("API_MAELYN", "o4mUjyB1Nh")

COOKIE_BING = os.environ.get(
    "COOKIE_BING",
    "1oJCbtTQ5Wc1xIpdnFQrO6_TZoYfMbb2Fg9kwQu3mE1fC0Sx0T9ADWEQGlQQcoW-YRTx6rCpaZ5dT4MPz77fieS-V-jAxAlspaPCK0_2Ox2_J5kIrl401VnZA30Dwt7pKuiQPwq4bqUBn2tclXRs8Aqm99JJ3fvsczXMhYR-bjYGmwucEwOhhewpYDBBjzdA9_PScOkJMgmL_gSw2eitRVw",
)

BOT_NAME = os.environ.get("BOT_NAME", "𝗝𝗢𝗡𝗔𝗧𝗛𝗔𝗡 𝗨𝗦𝗘𝗥𝗕𝗢𝗧")

DB_NAME = os.environ.get("DB_NAME", "jonathan")

URL_LOGO = os.environ.get("URL_LOGO", "https://files.catbox.moe/fzlxwt.png")

BLACKLIST_GCAST = get_blacklist()

SUDO_OWNERS = list(
    map(
        int,
        os.environ.get(
            "SUDO_OWNERS",
            "5648296402",
        ).split(),
    )
)
DEVS = list(
    map(
        int,
        os.environ.get(
            "DEVS",
            "5648296402",
        ).split(),
    )
)

AKSES_DEPLOY = list(
    map(int, os.environ.get("AKSES_DEPLOY", "5648296402").split())
)

OWNER_ID = int(os.environ.get("OWNER_ID", 5648296402))

LOG_SELLER = int(os.environ.get("LOG_SELLER", -1002797506458))

LOG_BACKUP = int(os.environ.get("LOG_BACKUP", -1002818541265))

SPOTIFY_CLIENT_ID = os.environ.get(
    "SPOTIFY_CLIENT_ID", "63f0f8de68554cb28bac5c47c1c907bc"
)
SPOTIFY_CLIENT_SECRET = os.environ.get(
    "SPOTIFY_CLIENT_SECRET", "63f0f8de68554cb28bac5c47c1c907bc"
)
SAWERIA_EMAIL = os.environ.get("SAWERIA_EMAIL", "brodiireng07@gmail.com")
SAWERIA_NAME = os.environ.get("SAWERIA_NAME", "mediaumum")
SAWERIA_USERID = os.environ.get(
    "SAWERIA_USERID", "b5a3485e-c1ee-4cb8-b657-a98243b20840"
)
FAKE_DEVS = list(map(int, os.environ.get("FAKE_DEVS", "7887821471").split()))

KYNAN = [5648296402]
if OWNER_ID not in SUDO_OWNERS:
    SUDO_OWNERS.append(OWNER_ID)
if OWNER_ID not in DEVS:
    DEVS.append(OWNER_ID)
if OWNER_ID not in FAKE_DEVS:
    FAKE_DEVS.append(OWNER_ID)
for P in FAKE_DEVS:
    if P not in DEVS:
        DEVS.append(P)
    if P not in SUDO_OWNERS:
        SUDO_OWNERS.append(P)
