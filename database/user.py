from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URL
client = AsyncIOMotorClient(MONGO_URL)
db = client["ResponseByAi"]

async def total_users():
    count = await userList.count_documents({})
    return count