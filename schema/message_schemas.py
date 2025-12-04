from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    recipient_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    created_at: datetime
    is_read: bool
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    last_message: Optional[str] = None
    unread_count: int = 0

class ConversationDetailResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    messages: list[MessageResponse]