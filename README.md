# Simple Direct Messaging Microservice

A minimal FastAPI microservice for direct messaging in a Game Catalog application.

## Features
- ✅ Send direct messages between users
- ✅ View conversation history  
- ✅ Mark messages as read
- ✅ Message encryption
- ✅ Integration with friends/notifications services

## Quick Start

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy cryptography httpx
   ```

2. Run the service:
   ```bash
   python main.py
   ```

3. API Documentation: http://localhost:8003/docs

## API Endpoints
- `POST /messages/send` - Send a message
- `GET /conversations/{user_id}` - Get user conversations
- `GET /messages/{conversation_id}` - Get conversation messages
- `PATCH /messages/{conversation_id}/read` - Mark messages as read

## User Stories Fulfilled

### Story 1: Direct Messaging
- ✅ Users can send messages to friends
- ✅ Messages delivered instantly
- ✅ Message history persists
- ✅ Messages encrypted

### Story 2: Message Notifications  
- ✅ Notifications sent for new messages
- ✅ Notifications cleared when read

## Files
- `main.py` - Main application and API routes
- `models.py` - Database models and schemas
- `database.py` - Database connection
- `services.py` - Business logic and external service calls