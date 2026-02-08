from fastapi import APIRouter, HTTPException, Header
from models.deployment import Deployment, DeploymentStatus
from models.request import CreateDeploymentRequest, UpdateStatusRequest
from services.policy_validator import validate_request
from services.pipeline_trigger import trigger_pipeline
from services.deployment_store import save, get_all, get_by_id, update_status
from services.ws_manager import manager
import os

PIPELINE_TOKEN = os.getenv("PIPELINE_TOKEN")

router = APIRouter(prefix="/deployments")


@router.post("/")
def create_deployment(request: CreateDeploymentRequest):
    """
    Receives a deployment request, validates it against policies,
    and if valid, creates a deployment record and triggers the execution pipeline.
    """
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

    # The state is now REQUESTED. Let's validate and transition.
    deployment.transition_to_validated()
    save(deployment)

    trigger_pipeline(deployment)

    return deployment.to_dict()

@router.get("/")
def list_deployments():
    return get_all()

@router.get("/{deployment_id}")
def get_deployment(deployment_id: str):
    deployment = get_by_id(deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Not found")
    return deployment

@router.patch("/{deployment_id}/status")
async def update_deployment_status(
    deployment_id: str,
    request: UpdateStatusRequest,
    x_pipeline_token: str = Header(None)
):
    # Simple security check to ensure only the pipeline calls this
    if x_pipeline_token !=PIPELINE_TOKEN:
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

    # Persist the new status and the latest event
    update_status(deployment.id, deployment.status.value, deployment.events[-1])

    await manager.broadcast({
        "deployment_id": deployment.id,
        "status": deployment.status.value
    })

    return deployment.to_dict()