import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongo_url = os.getenv("MONGO_URL")

client = MongoClient(mongo_url)

db = client["linkedin_insights"]

