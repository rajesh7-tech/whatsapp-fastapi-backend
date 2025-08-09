import json
from crud import insert_message, update_message_status
import os

def process_payload_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Drill down into the WhatsApp Cloud API webhook format
    entries = data.get("metaData", {}).get("entry", [])
    for entry in entries:
        for change in entry.get("changes", []):
            if change.get("field") == "messages":
                messages_arr = change.get("value", {}).get("messages", [])
                for msg in messages_arr:
                    try:
                        insert_message(msg)
                        print(f"Inserted message: {msg}")
                    except Exception as e:
                        print(f"Error inserting message: {e}")

            elif change.get("field") == "statuses":
                statuses_arr = change.get("value", {}).get("statuses", [])
                for status in statuses_arr:
                    try:
                        if "id" in status and "status" in status:
                            update_message_status(status["id"], status["status"])
                            print(f"Updated status: {status}")
                    except Exception as e:
                        print(f"Error updating message status: {e}")

if __name__ == "__main__":
    payload_folder = "payloads"
    for filename in os.listdir(payload_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(payload_folder, filename)
            print(f"Processing file: {filepath}")
            process_payload_file(filepath)
    print("Done processing all payloads.")
