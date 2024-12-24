from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from .routes import game

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Word Search Game API",
    description="API for generating and managing word search game puzzles",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include game routes
app.include_router(game.router, prefix="/api/game", tags=["game"])

@app.get("/")
async def root():
    return {"message": "Word Search Game API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 