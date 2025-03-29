from flask import Flask, jsonify
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

@app.route('/wooden')
def wooden_page():
    cursor = collection.find({"_id": {"$ne": doc_id}}).sort("timestamp", -1)

    wooden_data_list = []
    for doc in cursor:
        if "wooden" in doc:
            wooden_data_list.append(doc["wooden"])

    return jsonify({"wooden_data": wooden_data_list})

@app.route('/bfit')
def bfit_page():
    cursor = collection.find({"_id": {"$ne": doc_id}}).sort("timestamp", -1)

    bfit_data_list = []
    for doc in cursor:
        if "bfit" in doc:
            bfit_data_list.append(doc["bfit"])

    return jsonify({"bfit_data": bfit_data_list})

@app.route('/data')
def data_page():
    doc = collection.find_one({"_id": doc_id})
    doc["_id"] = str(doc["_id"])
    return jsonify(doc)

if __name__ == "__main__":
    app.run(debug=True)