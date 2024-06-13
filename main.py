import asyncio
import os


from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from loguru import logger

from modules.parsing import TelegramParseMessage
from modules.db import MongoAggregator
from modules.schemas import PeriodData

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
DB_NAME = "sampleDB"
DB_COLLECTION = "sample_collection"

logger.add("logs/{time}.log", rotation="10 MB")
db_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()
database = MongoAggregator(db_uri, DB_NAME, DB_COLLECTION)
parser = TelegramParseMessage()

@logger.catch
@dp.message(Command('start'))
async def start(message: types.Message):
    await message.reply(f"Привет, {message.from_user.username}!")

@logger.catch
@dp.message(F.text)
async def worker(message: types.Message):
    try:
        data = parser.get_data(message.text)
        logger.info(data)
        period_data = PeriodData(dt_from=data["dt_from"],
                                 dt_upto=data["dt_upto"],
                                 group_type=data["group_type"])
        result = await database.aggregate_data(period_data)
        logger.info(result)
        await message.answer(text=f"{result}")
    except Exception as e:
        logger.error(e)
        
@logger.catch
async def main():
    await dp.start_polling(bot)


asyncio.run(main())
