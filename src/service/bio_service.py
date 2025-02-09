from fastapi import FastAPI, WebSocket
from agent.agent import BioAgent
from pathlib import Path
import json
import uvicorn
class BioAgentService:
    def __init__(self, api_key: str):
        self.app = FastAPI()
        self.agent = BioAgent(api_key)
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.websocket("/ws/{client_id}")
        async def websocket_endpoint(websocket: WebSocket, client_id: str):
            await websocket.accept()
            while True:
                data = await websocket.receive_json()
                result = await self.agent.analyze_file(
                    Path(data["file_path"]),
                    data["content"]
                )
                await websocket.send_json(result)
        
    async def start(self, host: str = "127.0.0.1", port: int = 8000):
           await uvicorn.run(self.app, host=host, port=port)