from fastapi import APIRouter

router = APIRouter(prefix="/policies", tags=["Policies"])

POLICIES = [
    {
        "id": "POL-01",
        "name": "Production Approval",
        "severity": "HIGH",
        "status": "ACTIVE",
        "desc": "Deployments to production require approval"
    },
    {
        "id": "POL-02",
        "name": "Cost Allocation Tags",
        "severity": "MEDIUM",
        "status": "AUDIT",
        "desc": "All resources must have CostCenter and Owner tags"
    },
    {
        "id": "POL-03",
        "name": "Region Restriction",
        "severity": "HIGH",
        "status": "ACTIVE",
        "desc": "Deployments allowed only in approved regions"
    },
    {
        "id": "POL-04",
        "name": "Encryption Required",
        "severity": "HIGH",
        "status": "ACTIVE",
        "desc": "All storage must be encrypted at rest"
    },
    {
        "id": "POL-05",
        "name": "Instance Size Limit",
        "severity": "MEDIUM",
        "status": "ACTIVE",
        "desc": "Production cannot use large instance types"
    }
]

@router.get("/")
def list_policies():
    return POLICIES

@router.get("/settings")
def get_settings():
    return {
        "email_alerts": EMAIL_ALERTS,
        "slack_alerts": SLACK_ALERTS
    }
