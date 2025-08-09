from pymongo import MongoClient

MONGO_URI = "mongodb+srv://raju79972:Rajesh79972@whatsapp-mongodb.gvqobyz.mongodb.net/whatsapp?retryWrites=true&w=majority&appName=Whatsapp-Mongodb"
client = MongoClient(MONGO_URI)
db = client["whatsapp"]
processed_messages_collection = db["processed_messages"]

# Optional: Check connection
try:
	client.admin.command('ping')
	print("MongoDB connection successful.")
except Exception as e:
	print(f"MongoDB connection failed: {e}")
