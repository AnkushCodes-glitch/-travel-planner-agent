from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient = None

async def connect_db():
    global client
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    print("Connected to MongoDB")

async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_database():
    return client[settings.DATABASE_NAME]