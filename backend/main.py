import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from db import Base, engine
from routes import repo, code

load_dotenv()

# Allow both local dev and deployed frontend
origins = [
    "http://localhost:5173",                # local dev
    "https://ai-devops-agent-beta.vercel.app"  # deployed frontend (no trailing slash)
]

app = FastAPI(title="AI DevOps Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Which origins can talk to backend
    allow_credentials=True,
    allow_methods=["*"],         # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],         # Allow all headers
)

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app.include_router(repo.router, prefix="/repo", tags=["repo"])
app.include_router(code.router, prefix="/code", tags=["code"])
