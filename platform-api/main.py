from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers.deployments import router as deployment_router
from fastapi.middleware.cors import CORSMiddleware
from routers.policies import router as policy_router
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



app = FastAPI(title="Multi-Cloud Governance Platform")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

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

@app.get("/config")
def config():
    return {
        "demo_mode": DEMO_MODE
    }
