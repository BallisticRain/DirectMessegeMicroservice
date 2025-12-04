from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.message_models import Conversation, Message
from services.external_services import ExternalServices
from schema.message_schemas import MessageCreate, ConversationResponse
from datetime import datetime
import asyncio

class MessageController:
    """Controller for handling message business logic"""
    
    @staticmethod
    async def send_message(sender_id: int, message_data: MessageCreate, db: Session):
        """Send a direct message between users"""
        # Check friendship
        if not await ExternalServices.check_friendship(sender_id, message_data.recipient_id):
            raise HTTPException(status_code=403, detail="Users must be friends to message")
        
        # Get or create conversation
        user1, user2 = sorted([sender_id, message_data.recipient_id])
        conversation = db.query(Conversation).filter(
            Conversation.user1_id == user1, 
            Conversation.user2_id == user2
        ).first()
        
        if not conversation:
            conversation = Conversation(user1_id=user1, user2_id=user2)
            db.add(conversation)
            db.flush()
        
        # Create message
        message = Message(
            conversation_id=conversation.id,
            sender_id=sender_id,
            recipient_id=message_data.recipient_id,
            content=message_data.content
        )
        db.add(message)
        conversation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(message)
        
        # Send notification async
        asyncio.create_task(ExternalServices.send_notification(
            sender_id, message_data.recipient_id, message_data.content
        ))
        
        return message
    
    @staticmethod
    def get_conversations(user_id: int, db: Session):
        """Get user's conversations with unread counts"""
        conversations = db.query(Conversation).filter(
            (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
        ).order_by(Conversation.updated_at.desc()).all()
        
        result = []
        for conv in conversations:
            # Get last message
            last_msg = db.query(Message).filter(
                Message.conversation_id == conv.id
            ).order_by(Message.created_at.desc()).first()
            
            # Count unread messages
            unread = db.query(Message).filter(
                Message.conversation_id == conv.id,
                Message.recipient_id == user_id,
                Message.is_read == False
            ).count()
            
            result.append(ConversationResponse(
                id=conv.id,
                user1_id=conv.user1_id,
                user2_id=conv.user2_id,
                last_message=last_msg.content if last_msg else None,
                unread_count=unread
            ))
        
        return result
    
    @staticmethod
    def get_conversation_messages(conversation_id: int, user_id: int, db: Session):
        """Get messages in a specific conversation"""
        # Verify access
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        return {"conversation": conversation, "messages": messages}
    
    @staticmethod
    def mark_messages_as_read(conversation_id: int, user_id: int, db: Session):
        """Mark all messages in a conversation as read for a user"""
        updated = db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.recipient_id == user_id,
            Message.is_read == False
        ).update({Message.is_read: True})
        
        db.commit()
        
        print(f"✅ Marked {updated} messages as read for user {user_id}")
        
        return {"updated": updated}