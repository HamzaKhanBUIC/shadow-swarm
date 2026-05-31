from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables on startup
load_dotenv()

from agent_swarm import AgentSwarm

app = FastAPI(
    title="The Shadow Swarm - Overlord C2",
    description="Command & Control server for autonomous red teaming agents.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Mission(BaseModel):
    target: str
    objectives: list[str]

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.get("/")
def read_root():
    provider = os.getenv("LLM_PROVIDER", "mock").upper()
    return {
        "status": "Overlord C2 Online",
        "active_agents": len(manager.active_connections),
        "llm_provider": provider
    }

@app.post("/mission/launch")
async def launch_mission(mission: Mission):
    # 1. Broadcast mission start to all active websockets
    await manager.broadcast({
        "type": "MISSION_START",
        "target": mission.target,
        "status": "Swarm deployed"
    })
    
    # 2. Define real-time socket logger callback
    async def socket_log_callback(log_entry: dict):
        await manager.broadcast({
            "type": "AGENT_LOG",
            "log": log_entry
        })
        # Subtle sleep to allow UI log flow animations to breath
        await asyncio.sleep(0.1)
    
    # 3. Deploy the swarm and execute lifecycle
    swarm = AgentSwarm()
    results = await swarm.deploy_swarm(mission.target, socket_log_callback)
    
    # 4. Broadcast mission completion and results
    await manager.broadcast({
        "type": "MISSION_COMPLETE",
        "target": mission.target,
        "results": results
    })
    
    return {"message": "Mission completed successfully", "mission": mission, "results": results}

@app.websocket("/ws/console")
async def websocket_console(websocket: WebSocket):
    """WebSocket for the Next.js UI to receive real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Receive commands from console if needed (currently read and echo)
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
