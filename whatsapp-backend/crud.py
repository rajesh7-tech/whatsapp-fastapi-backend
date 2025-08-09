from database import processed_messages_collection
from bson.objectid import ObjectId

def get_all_conversations():
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {
            "$group": {
                "_id": "$from",
                "last_message": {"$first": "$$ROOT"},
                "count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "wa_id": "$_id",
                "last_message": 1,
                "count": 1,
                "_id": 0,
            }
        },
        {"$limit": 50}
    ]
    results = list(processed_messages_collection.aggregate(pipeline))
    for conv in results:
        conv["name"] = "User " + conv["wa_id"][-4:]
        lm = conv.get("last_message", {})
        lm["id"] = str(lm.get("_id"))
        if "_id" in lm:
            del lm["_id"]
    return results

def insert_message(message_dict):
    return processed_messages_collection.insert_one(message_dict)

def get_messages_by_wa_id(wa_id):
    messages = list(processed_messages_collection.find({"from": wa_id}).sort("timestamp", 1))
    for msg in messages:
        msg["id"] = str(msg["_id"])
        if "_id" in msg:
            del msg["_id"]
    return messages

def update_message_status(message_id, new_status):
    return processed_messages_collection.update_one(
        {"_id": ObjectId(message_id)}, {"$set": {"status": new_status}}
    )
