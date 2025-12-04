import httpx
import asyncio

class ExternalServices:
    """Service for communicating with external microservices"""
    
    @staticmethod
    async def check_friendship(user1_id: int, user2_id: int) -> bool:
        """Check if users are friends using the actual Friends microservice"""
        try:
            async with httpx.AsyncClient() as client:
                # Get friends list for user1
                response = await client.get(
                    "http://localhost:8000/my-friends",
                    headers={"X-User-ID": str(user1_id)},
                    timeout=2.0
                )
                if response.status_code == 200:
                    friends_data = response.json()
                    friend_ids = [friend["user_id"] for friend in friends_data.get("friends", [])]
                    return user2_id in friend_ids
        except Exception as e:
            print(f"Friends service error: {e}")
        return True  # Allow messaging if friends service is down
    
    @staticmethod
    async def send_notification(sender_id: int, recipient_id: int, message: str):
        """Send notification using Kenneth's notification service"""
        try:
            async with httpx.AsyncClient() as client:
                # Kenneth's service expects RabbitMQ messages, but we'll try direct HTTP
                notification_data = {
                    "senderId": sender_id,
                    "receiverId": recipient_id,
                    "entityId": 0,  # Message ID - we'll use 0 for now
                    "type": "message",
                    "message": f"New message: {message[:50]}"
                }
                
                # Try to send directly to the notification service
                await client.post(
                    "http://localhost:8030/notify/notifications",
                    json=notification_data,
                    timeout=1.0
                )
                print(f"📧 Notification sent to user {recipient_id}: {message[:30]}...")
        except Exception as e:
            print(f"Notification service unavailable: {e}")
            # Mock notification for development
            print(f"📱 [MOCK] User {recipient_id} would receive notification: '{message[:50]}'")
            pass  # Silent fail for notifications