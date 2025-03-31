import requests
from datetime import datetime, timezone, time
import pytz
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def load_data(): 
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
        'AccountAPIKey': os.getenv("API_KEY"),
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

            wooden["added_date"] = {
                "original_date": dt,
                "formatted_date": formatted_date,
                "formatted_time": formatted_time,
            }

            wooden[entry["LocationName"]] = {
                "closed": entry["IsClosed"],
                "capacity": capacity,
                "count": count,
                "percentage": percentage
            }

            overall = helper_overall_occupancy(wooden)
            wooden["all_zones"] = {
                "count": overall["count"],
                "capacity": overall["capacity"],
                "percentage": overall["percentage"]
            }

        if entry["FacilityName"] == "Bruin Fitness Center - FITWELL":
            dt = datetime.fromisoformat(entry["LastUpdatedDateAndTime"])
            formatted_date = dt.strftime("%m/%d/%Y")
            formatted_time = dt.strftime("%-I:%M %p")

            capacity = entry["TotalCapacity"]
            count = entry["LastCount"]

            percentage = int(round((count / capacity) * 100)) if capacity else 0

            bfit["added_date"] = {
                "original_date": dt,
                "formatted_date": formatted_date,
                "formatted_time": formatted_time,
            }

            bfit[entry["LocationName"]] = {
                "closed": entry["IsClosed"],
                "capacity": capacity,
                "count": count,
                "percentage": percentage,
            }
            
            overall = helper_overall_occupancy(bfit)

            bfit["all_zones"] = {
                "count": overall["count"],
                "capacity": overall["capacity"],
                "percentage": overall["percentage"]
            }
    
    return [wooden, bfit]

def update_cell(gym_data):
    MONGO_URI = os.getenv("MONGODB_URI")
    print("Connecting to:")
    client = MongoClient(MONGO_URI)
    db = client["UclaGym"]
    collection = db["gym-occupancy"]

    doc_id = ObjectId("67e73b40070de1e22fd7463e")
    doc = collection.find_one({"_id": doc_id})

    wooden_dt = gym_data[0]["added_date"]["original_date"]
    wooden_day = wooden_dt.strftime("%A").lower()
    wooden_time = wooden_dt.strftime("%H:00:00")

    bfit_dt = gym_data[1]["added_date"]["original_date"]
    bfit_day = bfit_dt.strftime("%A").lower()
    bfit_time = bfit_dt.strftime("%H:00:00")

    wooden_entries = doc["wooden"][wooden_day][wooden_time]["entries"]
    wooden_prev_occupancy = doc["wooden"][wooden_day][wooden_time]["occupancy"]

    bfit_entries = doc["bfit"][bfit_day][bfit_time]["entries"]
    bfit_prev_occupancy = doc["bfit"][bfit_day][bfit_time]["occupancy"]

    wooden_new_occupancy = ((wooden_prev_occupancy * wooden_entries) + gym_data[0]["all_zones"]["percentage"]) / (wooden_entries + 1)
    wooden_new_occupancy = round(wooden_new_occupancy, 2)

    bfit_new_occupancy = ((bfit_prev_occupancy * bfit_entries) + gym_data[1]["all_zones"]["percentage"]) / (bfit_entries + 1)
    bfit_new_occupancy = round(bfit_new_occupancy, 2)

    wooden_entries_path = f"{"wooden"}.{wooden_day}.{wooden_time}.entries"
    wooden_occupancy_path = f"{"wooden"}.{wooden_day}.{wooden_time}.occupancy"

    bfit_entries_path = f"{"bfit"}.{bfit_day}.{bfit_time}.entries"
    bfit_occupancy_path = f"{"bfit"}.{bfit_day}.{bfit_time}.occupancy"

    collection.update_one(
        {"_id": doc_id},
        {
            "$inc": {wooden_entries_path: 1,
                     bfit_entries_path: 1},
            "$set": {wooden_occupancy_path: wooden_new_occupancy,
                     bfit_occupancy_path: bfit_new_occupancy}
        }
    )

def add_hour(gym_data):
    MONGO_URI = os.getenv("MONGODB_URI")
    print("Connecting to:")
    client = MongoClient(MONGO_URI)
    db = client["UclaGym"]
    collection = db["gym-occupancy"]

    tz = pytz.timezone("America/Los_Angeles")
    now = datetime.now(tz)

    formatted_date = now.strftime("%m/%d")
    formatted_hour = now.strftime("%H:00:00")

    doc = {
        "formatted_date": formatted_date,
        "formatted_hour": formatted_hour,
        "wooden": gym_data[0],
        "bfit": gym_data[1]
    }

    filter_expr = {
        "formatted_date": doc["formatted_date"],
        "formatted_hour": doc["formatted_hour"]
    }

    collection.replace_one(
        filter_expr,
        doc,
        upsert=True
    )

def helper_overall_occupancy(gym):
    total_count = 0
    total_capacity = 0

    for zone_name, data in gym.items():
        if data.get("closed"):
            continue 

        count = data.get("count", 0)
        capacity = data.get("capacity", 0)

        total_count += count
        total_capacity += capacity

    if total_capacity == 0:
        overall_percentage = 0
    else:
        overall_percentage = round((total_count / total_capacity) * 100, 2)

    return {
        "count": total_count,
        "capacity": total_capacity,
        "percentage": overall_percentage
    }

if __name__ == "__main__":
    res = load_data()
    update_cell(res)
    add_hour(res)