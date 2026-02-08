from fastapi import WebSocket
import json

class WSManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, data: dict):
        dead = []
        for conn in self.connections:
            try:
                await conn.send_text(json.dumps(data))
            except:
                dead.append(conn)

        for d in dead:
            self.disconnect(d)

manager = WSManager()
