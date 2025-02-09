from fastapi import WebSocket
from typing import Dict, Any
from agent.agent import BioAgent
import json
import logging
from datetime import datetime
from pathlib import Path

class WebSocketHandler:
    def __init__(self, agent: BioAgent):
        self.agent = agent
        self.logger = logging.getLogger(__name__)
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.logger.info(f"Client {client_id} connected")
        
    async def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            self.logger.info(f"Client {client_id} disconnected")
            
    async def handle_message(self, websocket: WebSocket, client_id: str):
        try:
            while True:
                message = await websocket.receive_json()
                
                response = await self.process_message(message, client_id)
                await websocket.send_json(response)
                
        except Exception as e:
            self.logger.error(f"Error handling message from {client_id}: {str(e)}")
            await self.disconnect(client_id)
            
    async def process_message(self, message: Dict, client_id: str) -> Dict[str, Any]:
        # Direct passthrough to existing agent capabilities
        result = await self.agent.analyze_file(
            Path(message["file_path"]),
            message["content"]
        )
        
        return {
            "type": "analysis_result",
            "result": result,
            "client_id": client_id
        }