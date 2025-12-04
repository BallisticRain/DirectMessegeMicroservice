"""Simple test script for the messaging API"""

import asyncio
import httpx

async def test_messaging_api():
    """Test the messaging service endpoints"""
    
    print("🚀 Testing Direct Messaging API")
    print("=" * 40)
    
    base_url = "http://localhost:8003"
    
    async with httpx.AsyncClient() as client:
        try:
            # Test health
            print("1. Testing health endpoint...")
            response = await client.get(f"{base_url}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Send a message
            print("\n2. Sending test message...")
            message_data = {
                "recipient_id": 2,
                "content": "Hello! This is a test message."
            }
            response = await client.post(
                f"{base_url}/api/messages/send",
                params={"sender_id": 1},
                json=message_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                msg = response.json()
                print(f"   Message ID: {msg['id']}")
                print(f"   Content: {msg['content']}")
            
            # Get conversations
            print("\n3. Getting conversations...")
            response = await client.get(
                f"{base_url}/api/messages/conversations",
                params={"user_id": 1}
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                conversations = response.json()
                print(f"   Found {len(conversations)} conversations")
                for conv in conversations:
                    print(f"     - Conversation {conv['id']}: Users {conv['user1_id']} & {conv['user2_id']}")
            
            # Get messages (assume conversation ID 1 exists)
            print("\n4. Getting messages...")
            response = await client.get(
                f"{base_url}/api/messages/conversations/1",
                params={"user_id": 1}
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Found {len(data['messages'])} messages")
                for msg in data['messages']:
                    print(f"     - From User {msg['sender_id']}: {msg['content'][:30]}...")
            
            print("\n✅ All tests completed!")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Make sure the service is running with: python main.py")
    print()
    asyncio.run(test_messaging_api())