from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from crud import (
    get_all_conversations,
    get_messages_by_wa_id,
    insert_message,
    update_message_status,
)
from bson.objectid import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    from_: str = Field(..., alias="from")
    id: Optional[str]
    timestamp: str
    text: dict
    type: str
    status: Optional[str] = None  # Optional status field

    class Config:
        allow_population_by_field_name = True

class Conversation(BaseModel):
    wa_id: str
    name: Optional[str] = None
    last_message: Optional[Message] = None

@app.get("/api/conversations", response_model=List[Conversation])
def list_conversations():
    return get_all_conversations()

@app.post("/api/message")
def add_message(msg: Message):
    # Set default status to 'sending' if not provided
    if not msg.status:
        msg.status = "sending"
    msg_dict = msg.dict(by_alias=True)
    try:
        result = insert_message(msg_dict)
        if result.inserted_id:
            # Update message status to 'sent' immediately after successful insert
            update_message_status(str(result.inserted_id), "sent")
            return {"status": "success", "id": str(result.inserted_id)}
        else:
            return {"status": "failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/messages/{wa_id}", response_model=List[Message])
def get_messages(wa_id: str):
    return get_messages_by_wa_id(wa_id)

@app.patch("/api/message/status/{message_id}")
def update_status(message_id: str, status_update: dict):
    new_status = status_update.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="Status is required")
    result = update_message_status(message_id, new_status)
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"status": "updated"}
