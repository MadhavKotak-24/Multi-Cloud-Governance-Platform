import yaml
import re
import os

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POLICY_FILE = os.path.join(
    BASE_DIR,
    "policies",
    "deployment-policy.yaml"
)



def load_policy():
    with open(POLICY_FILE, "r") as f:
        return yaml.safe_load(f)


def validate_request(cloud, environment, application):
    policy = load_policy()

    # Cloud validation
    if cloud not in policy["allowed_clouds"]:
        raise ValueError(f"Cloud '{cloud}' not allowed by policy")

    # Environment validation
    if environment not in policy["allowed_environments"]:
        raise ValueError(f"Environment '{environment}' not allowed")

    # Production rule
    if environment == "prod" and policy["rules"]["production_requires_approval"]:
        raise ValueError("Production deployments require approval")

    # App name length
    if len(application) < policy["application"]["min_length"]:
        raise ValueError("Application name too short")

    if len(application) > policy["rules"]["max_app_name_length"]:
        raise ValueError("Application name too long")

    # Naming convention
    pattern = policy["application"]["allowed_pattern"]
    if not re.match(pattern, application):
        raise ValueError(
            "Application name must be lowercase, numbers, and hyphens only"
        )

    return True

