from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv
import sys

# Add src to Python path
sys.path.append(str(Path(__file__).parent))
from agent.agent import BioAgent

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = BioAgent(api_key=os.getenv("GROQ_API_KEY"))

@app.post("/chat")
async def chat(message: str):
    response = await agent.chat(message)
    return {"response": response}

@app.post("/analyze")
async def analyze(file_path: str):
    results = await agent.analyze_file(Path(file_path), "analyze")
    return results