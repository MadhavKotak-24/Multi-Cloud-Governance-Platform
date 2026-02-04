from fastapi import APIRouter

router = APIRouter(prefix="/policies", tags=["Policies"])

@router.get("")
def list_policies():
    return [
        {
            "id": "POL-01",
            "name": "Production Approval",
            "desc": "Deployments to production require approval",
            "severity": "HIGH",
            "status": "ACTIVE"
        },
        {
            "id": "POL-02",
            "name": "Cost Allocation Tags",
            "desc": "All resources must have CostCenter tags",
            "severity": "MEDIUM",
            "status": "AUDIT"
        }
    ]