import yaml
import re

POLICY_FILE = "../policies/deployment-policy.yaml"

def load_policy():
    with open(POLICY_FILE, "r") as f:
        return yaml.safe_load(f)

def validate_request(cloud, environment, application):
    policy = load_policy()

    if cloud not in policy["allowed_clouds"]:
        raise ValueError("Cloud not allowed by policy")

    if environment not in policy["allowed_environments"]:
        raise ValueError("Environment not allowed by policy")

    if len(application) < policy["application"]["min_length"]:
        raise ValueError("Application name too short")

    pattern = policy["application"]["allowed_pattern"]
    if not re.match(pattern, application):
        raise ValueError("Application name violates naming policy")

    return True
