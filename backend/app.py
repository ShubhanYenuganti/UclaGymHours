from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["UclaGym"]
collection = db["gym-occupany"]

@app.route('/api')
def root_page():
    doc = collection.find_one(sort=[("timestamp", -1)])
    return jsonify({
        "timestamp": doc["timestamp"],
        "wooden": doc["wooden"],
        "bfit": doc["bfit"]
    })


if __name__ == "__main__":
    app.run(debug=True)