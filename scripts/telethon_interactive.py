from pathlib import Path
import json
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

CONFIG = json.load(open(Path.cwd().joinpath("src/config.json")))

client = TelegramClient(
    session=StringSession(),
    api_id=CONFIG["TELETHON"]["API_ID"],
    api_hash=CONFIG["TELETHON"]["API_HASH"],
).start()


me = client.get_me()
print(me.stringify())
