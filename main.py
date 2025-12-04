"""
Direct Messaging Microservice
Modular Architecture - Similar to Friends Service
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.config import engine, Base
from router.message_router import message_router

# FastAPI app
app = FastAPI(title="Direct Messaging Microservice")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(message_router)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Direct Messaging Microservice...")
    print("📧 Running with external service integration")
    print("🤝 Friends service: http://localhost:8000")
    print("📱 Notifications service: http://localhost:8030")
    uvicorn.run(app, host="0.0.0.0", port=8003)