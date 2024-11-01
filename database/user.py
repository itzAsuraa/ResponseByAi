from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URL
client = AsyncIOMotorClient(MONGO_URL)
db = client["ResponseByAi"]
userList = db.userList

async def total_users():
    count = await userList.count_documents({})
    return count

def addUser(userId , userName):
    dets = {
        'userId': userId,
        'userName': userName
    }
    userList.insert_one(dets).inserted_id
    return