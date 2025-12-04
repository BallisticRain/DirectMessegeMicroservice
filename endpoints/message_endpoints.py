from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schema.message_schemas import MessageCreate, MessageResponse, ConversationResponse
from controllers.message_controller import MessageController
from database.config import get_db
from typing import List

def health_check():
    """Health check endpoint"""
    return {"status": "Direct Messaging Microservice Running"}

async def send_message_endpoint(
    sender_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """Send a direct message"""
    return await MessageController.send_message(sender_id, message_data, db)

def get_conversations_endpoint(
    user_id: int,
    db: Session = Depends(get_db)
) -> List[ConversationResponse]:
    """Get user's conversations"""
    return MessageController.get_conversations(user_id, db)

def get_conversation_messages_endpoint(
    conversation_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get messages in a conversation"""
    return MessageController.get_conversation_messages(conversation_id, user_id, db)

def mark_messages_read_endpoint(
    conversation_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Mark messages as read"""
    return MessageController.mark_messages_as_read(conversation_id, user_id, db)