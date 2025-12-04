from fastapi import APIRouter
from endpoints.message_endpoints import (
    health_check,
    send_message_endpoint,
    get_conversations_endpoint,
    get_conversation_messages_endpoint,
    mark_messages_read_endpoint
)

# Create router
message_router = APIRouter()

# Health check
message_router.add_api_route("/health", health_check, methods=["GET"])

# Message endpoints
message_router.add_api_route("/api/messages/send", send_message_endpoint, methods=["POST"])
message_router.add_api_route("/api/messages/conversations", get_conversations_endpoint, methods=["GET"])
message_router.add_api_route("/api/messages/conversations/{conversation_id}", get_conversation_messages_endpoint, methods=["GET"])
message_router.add_api_route("/api/messages/conversations/{conversation_id}/read", mark_messages_read_endpoint, methods=["PATCH"])