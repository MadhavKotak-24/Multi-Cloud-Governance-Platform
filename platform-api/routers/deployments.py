from fastapi import APIRouter, HTTPException, Header, Depends
from models.deployment import Deployment, DeploymentStatus
from models.request import CreateDeploymentRequest, UpdateStatusRequest
from services.policy_validator import validate_request
from services.pipeline_trigger import trigger_pipeline
from services.deployment_store import save, get_all, get_by_id, update_status
from services.auth import create_token, DEMO_USER, get_current_user
from pydantic import BaseModel
import os
import uuid
from datetime import datetime

PIPELINE_TOKEN = os.getenv("PIPELINE_TOKEN")

# ===============================
# DEMO MODE CONFIG
# ===============================
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

DEMO_DEPLOYMENTS = {}

DEMO_STAGES = [
    "REQUESTED",
    "VALIDATED",
    "IN_PROGRESS",
    "SUCCESS"
]

STAGE_INTERVAL = 3  # seconds per stage


router = APIRouter(prefix="/deployments")

@router.get("/config")
def get_config():
    """Returns the demo mode status for the frontend."""
    return {"demo_mode": DEMO_MODE}

@router.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

# ---------------- LOGIN ---------------- #

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(req: LoginRequest):
    if req.username != DEMO_USER["username"] or req.password != DEMO_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(req.username)
    return {"token": token}

# ---------------- DEPLOYMENTS ---------------- #

@router.post("/")
def create_deployment(
    request: CreateDeploymentRequest,
    user=Depends(get_current_user)   # protect
):
    try:
        validate_request(
            request.cloud,
            request.environment,
            request.application
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # ===============================
    # DEMO MODE PATH
    # ===============================
    if DEMO_MODE:
        dep_id = f"DEP-{uuid.uuid4().hex[:6].upper()}"

        DEMO_DEPLOYMENTS[dep_id] = {
            "id": dep_id,
            "cloud": request.cloud,
            "environment": request.environment,
            "application": request.application,
            "created_at": datetime.now(),
        }

        return {
            "id": dep_id,
            "cloud": request.cloud,
            "environment": request.environment,
            "application": request.application,
            "status": "REQUESTED",
            "created_at": datetime.now().isoformat(),
            "events": [
                {
                    "status": "REQUESTED",
                    "time": datetime.utcnow().isoformat()
                }
            ]
        }
    
    # ===============================
    # REAL PATH (unchanged)
    # ===============================

    deployment = Deployment(
        request.cloud,
        request.environment,
        request.application
    )

    deployment.transition_to_validated()
    save(deployment)

    trigger_pipeline(deployment)

    return deployment.to_dict()


@router.get("/")
def list_deployments(user=Depends(get_current_user)):

    # ===============================
    # DEMO MODE PATH
    # ===============================
    if DEMO_MODE:
        results = []

        for dep in DEMO_DEPLOYMENTS.values():
            elapsed = (datetime.utcnow() - dep["created_at"]).total_seconds()
            stage_index = min(int(elapsed // STAGE_INTERVAL), len(DEMO_STAGES) - 1)

            status = DEMO_STAGES[stage_index]

            events = []
        for i in range(stage_index + 1):
            stage_time = dep["created_at"] + timedelta(seconds=i * STAGE_INTERVAL)

            events.append({
                "status": DEMO_STAGES[i],
                "time": stage_time.isoformat()
            })

            results.append({
                "id": dep["id"],
                "cloud": dep["cloud"],
                "environment": dep["environment"],
                "application": dep["application"],
                "status": status,
                "created_at": dep["created_at"].isoformat(),
                "events": events
            })

        return results

    # ===============================
    # REAL PATH
    # ===============================

    return get_all()


@router.get("/{deployment_id}")
def get_deployment(deployment_id: str, user=Depends(get_current_user)):
    deployment = get_by_id(deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Not found")
    return deployment


@router.patch("/{deployment_id}/status")
def update_deployment_status(
    deployment_id: str,
    request: UpdateStatusRequest,
    x_pipeline_token: str = Header(None)
):
    if x_pipeline_token != PIPELINE_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = get_by_id(deployment_id)
    if not data:
        raise HTTPException(status_code=404, detail="Deployment not found")

    deployment = Deployment.from_dict(data)

    try:
        new_status = DeploymentStatus(request.status)
        deployment.transition(new_status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    update_status(deployment.id, deployment.status.value, deployment.events[-1])

    return deployment.to_dict()
