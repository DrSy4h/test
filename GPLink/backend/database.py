"""
GPLink - Database Connection
MongoDB connection setup for GPLink consultation system
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGODB_ATLAS_CLUSTER_URI")
db_name = os.getenv("MONGODB_DATABASE_NAME", "gplink_db")

# MongoDB Client
client = MongoClient(mongo_uri)
db = client[db_name]

# Collections
consultations_collection = db["consultations"]
doctors_collection = db["doctors"]

# Create indexes
consultations_collection.create_index("consultation_id", unique=True)
consultations_collection.create_index("status")
doctors_collection.create_index("email", unique=True)

print(f"✅ Connected to MongoDB: {db_name}")
