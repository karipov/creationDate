from pathlib import Path
import json

from aiogram import Bot, Dispatcher, executor, types


# Load configuration
CONFIG = json.load(open(Path.cwd().joinpath("src/config.json")))


# Initialize
bot = Bot(token=CONFIG["AIOGRAM"]["TOKEN"])
dp = Dispatcher(bot=bot)


# Catch-all message handler
@dp.message_handler()
async def down(message: types.Message):
    await message.answer(
        "The bot is currently down for maintenance. Please be patient, it "
        "will be up soon."
    )


# Polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
