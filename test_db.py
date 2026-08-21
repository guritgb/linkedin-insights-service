import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongo_url = os.getenv("MONGO_URL")

client = MongoClient(mongo_url)

try:
    client.admin.command("ping")
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed:", e)
finally:
    client.close()