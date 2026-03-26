# import os
# from contextlib import asynccontextmanager

# from dotenv import load_dotenv
# from fastapi import FastAPI
# from motor.motor_asyncio import AsyncIOMotorClient

# # Load .env from the same directory as this file
# load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


# class MongoDB:
#     client: AsyncIOMotorClient | None = None
#     db = None


# db_helper = MongoDB()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     mongodb_url = os.getenv("MONGODB_URL")
#     if not mongodb_url:
#         raise RuntimeError("MONGODB_URL is not configured.")

#     # Startup: connect to Atlas
#     db_helper.client = AsyncIOMotorClient(mongodb_url)
#     db_helper.db = db_helper.client.get_database("autovibe_db")

#     try:
#         await db_helper.client.admin.command("ping")
#         print("Successfully connected to MongoDB Atlas!")
#     except Exception as e:
#         print(f"Error connecting to MongoDB: {e}")

#     yield

#     # Shutdown: close connection
#     if db_helper.client:
#         db_helper.client.close()
#         print("MongoDB connection closed.")


# def get_vehicle_collection():
#     return db_helper.db.get_collection("vehicles")


# def get_negotiation_collection():
#     return db_helper.db.get_collection("negotiations")











import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

# Load .env from the same directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class MongoDB:
    client: AsyncIOMotorClient | None = None
    db = None

db_helper = MongoDB()

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise RuntimeError("MONGODB_URL is not configured in .env")

    # Startup: connect to Atlas
    db_helper.client = AsyncIOMotorClient(mongodb_url)
    db_helper.db = db_helper.client.get_database("autovibe_db")

    try:
        await db_helper.client.admin.command("ping")
        print("🚀 Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")

    yield

    # Shutdown: close connection
    if db_helper.client:
        db_helper.client.close()
        print("🔒 MongoDB connection closed.")

def get_vehicle_collection():
    return db_helper.db.get_collection("vehicles")

def get_user_collection():
    return db_helper.db.get_collection("users")

def get_negotiations_collection():
    return db_helper.db.get_collection("negotiations")