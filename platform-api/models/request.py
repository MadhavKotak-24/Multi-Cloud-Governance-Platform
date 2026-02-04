from pydantic import BaseModel, Field

class CreateDeploymentRequest(BaseModel):
    application: str = Field(..., example="sample-app")
    cloud: str = Field(..., example="aws")
    environment: str = Field(..., example="dev")

class UpdateStatusRequest(BaseModel):
    status: str = Field(..., example="SUCCESS")