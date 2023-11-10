import motor.motor_asyncio
from core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB)
db = client.rss
collection = db.users
