import requests
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv
import os

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.connect2mycloud.com',
    'Referer': 'https://www.connect2mycloud.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not:A-Brand";v="24", "Chromium";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'AccountAPIKey': '73829a91-48cb-4b7b-bd0b-8cf4134c04cd',
}

response = requests.get(
    'https://goboardapi.azurewebsites.net/api/FacilityCount/GetCountsByAccount',
    params=params,
    headers=headers,
)

data = response.json()

wooden = {}
bfit = {}

for entry in data:
    if entry["FacilityName"] == "John Wooden Center - FITWELL":
        dt = datetime.fromisoformat(entry["LastUpdatedDateAndTime"])
        formatted_date = dt.strftime("%m/%d/%Y")
        formatted_time = dt.strftime("%-I:%M %p")

        capacity = entry["TotalCapacity"]
        count = entry["LastCount"]

        percentage = int(round((count / capacity) * 100)) if capacity else 0

        wooden[entry["LocationName"]] = {
            "closed": entry["IsClosed"],
            "capacity": capacity,
            "count": count,
            "percentage": percentage,
            "formatted_date": formatted_date,
            "formatted_time": formatted_time
        }

    if entry["FacilityName"] == "Bruin Fitness Center - FITWELL":
        dt = datetime.fromisoformat(entry["LastUpdatedDateAndTime"])
        formatted_date = dt.strftime("%m/%d/%Y")
        formatted_time = dt.strftime("%-I:%M %p")

        capacity = entry["TotalCapacity"]
        count = entry["LastCount"]

        percentage = int(round((count / capacity) * 100)) if capacity else 0

        bfit[entry["LocationName"]] = {
            "closed": entry["IsClosed"],
            "capacity": capacity,
            "count": count,
            "percentage": percentage,
            "formatted_date": formatted_date,
            "formatted_time": formatted_time
        }


# Connect to MongoDB
MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["UclaGym"]
collection = db["gym-occupany"]

doc = {
    "timestamp": datetime.now(timezone.utc),
    "wooden": wooden,
    "bfit": bfit
}

collection.insert_one(doc)