from fastapi import APIRouter, HTTPException, Header, Depends
from models.deployment import Deployment, DeploymentStatus
from models.request import CreateDeploymentRequest, UpdateStatusRequest
from services.policy_validator import validate_request
from services.pipeline_trigger import trigger_pipeline
from services.deployment_store import save, get_all, get_by_id, update_status
from services.auth import create_token, DEMO_USER, get_current_user
from pydantic import BaseModel
import os

PIPELINE_TOKEN = os.getenv("PIPELINE_TOKEN")

router = APIRouter(prefix="/deployments")

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
