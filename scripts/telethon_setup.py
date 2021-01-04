from pathlib import Path
import json
from telethon import TelegramClient

CONFIG = json.load(open(Path.cwd().joinpath("src/config.json")))

client = TelegramClient(
    session=str(Path.cwd().joinpath(CONFIG["TELETHON"]["SESSION"])),
    api_id=CONFIG["TELETHON"]["API_ID"],
    api_hash=CONFIG["TELETHON"]["API_HASH"],
)


async def main():
    me = await client.get_me()
    print(me.stringify())


with client:
    client.loop.run_until_complete(main())
