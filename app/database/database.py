from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

MONGO_DB_URL = settings.MONGO_DB_URL
DATABASE_NAME = settings.DATABASE_NAME

client = AsyncIOMotorClient(MONGO_DB_URL,tls=True)
db = client[DATABASE_NAME]

# Collection reference 
registration_collection = db["registrations"]
