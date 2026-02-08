from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from routers.deployments import router as deployment_router
from fastapi.middleware.cors import CORSMiddleware
from routers.policies import router as policy_router
from dotenv import load_dotenv

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Multi-Cloud Governance Platform")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev-only, safe for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deployment_router)
app.include_router(policy_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Cloud Governance API running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

