from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

app = Flask(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["UclaGym"]
collection = db["gym-occupancy"]
doc_id = ObjectId("67e73b40070de1e22fd7463e")


@app.route('/')
def rootpage():
    # doc = collection.find_one({"_id": doc_id})
    # doc["_id"] = str(doc["_id"])
    # return jsonify(doc)

    return render_template("home.html")

@app.route('/wooden')
def wooden_page():
    cursor = collection.find({"_id": {"$ne": doc_id}}).sort("timestamp", -1)

    wooden_data_list = []
    for doc in cursor:
        if "wooden" in doc:
            wooden_data_list.append(doc["wooden"])

    hourly_percentages = parse_hourly_percentages(wooden_data_list)
    return render_template("hourly.html", gym="Wooden", data=hourly_percentages)

@app.route('/bfit')
def bfit_page():
    cursor = collection.find({"_id": {"$ne": doc_id}}).sort("timestamp", -1)

    bfit_data_list = []
    for doc in cursor:
        if "bfit" in doc:
            bfit_data_list.append(doc["bfit"])

    hourly_percentages = parse_hourly_percentages(bfit_data_list)
    return render_template("hourly.html", gym="BFit", data=hourly_percentages)

def parse_hourly_percentages(data):
    hourly = {}
    for entry in data:
        added_date = entry.get("added_date", {}).get("original_date")
        percentage = entry.get("all_zones", {}).get("percentage")

        if not added_date or percentage is None:
            continue

        dt = added_date
        hour_key = f"{dt.hour:02d}:00:00"
        hourly[hour_key] = percentage

    return dict(sorted(hourly.items()))

if __name__ == "__main__":
    app.run(debug=True)
