from enum import Enum
from datetime import datetime, timezone
from uuid import uuid4

class DeploymentStatus(str, Enum):
    REQUESTED = "REQUESTED"
    VALIDATED = "VALIDATED"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
ALLOWED_TRANSITIONS = {
    DeploymentStatus.REQUESTED: [DeploymentStatus.VALIDATED],
    DeploymentStatus.VALIDATED: [DeploymentStatus.IN_PROGRESS],
    DeploymentStatus.IN_PROGRESS: [
        DeploymentStatus.SUCCESS,
        DeploymentStatus.FAILED
    ]
}
class Deployment:
    def __init__(self, cloud, environment, application):
        self.id = str(uuid4())
        self.cloud = cloud
        self.environment = environment
        self.application = application
        self.status = DeploymentStatus.REQUESTED
        self.created_at=datetime.now(timezone.utc).isoformat()
        self.events = [
            {
                "status": self.status,
                "time":self.created_at
            }
        ]

    @classmethod
    def from_dict(cls, data):
        obj = cls.__new__(cls)
        obj.id = data["id"]
        obj.cloud = data["cloud"]
        obj.environment = data["environment"]
        obj.application = data["application"]
        obj.status = DeploymentStatus(data["status"])
        obj.created_at = data["created_at"]
        obj.events = data["events"]
        return obj

    def transition_to_validated(self):
        self.transition(DeploymentStatus.VALIDATED)

    def transition(self, new_status):
        allowed = ALLOWED_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Invalid state transition {self.status} → {new_status}"
            )

        self.status = new_status
        self.events.append({
            "status": new_status,
            "time": datetime.now(timezone.utc).isoformat()
        })

    def to_dict(self):
        return {
            "id": self.id,
            "cloud": self.cloud,
            "environment": self.environment,
            "application": self.application,
            "status": self.status.value,
            "created_at": self.created_at,
            "events": self.events
        }
