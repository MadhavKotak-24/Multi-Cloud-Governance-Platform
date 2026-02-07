import os
import requests

def trigger_github_pipeline(deployment):
    token = os.environ.get("GITHUB_TOKEN")
    owner = os.environ.get("REPO_OWNER")
    repo = os.environ.get("REPO_NAME")

    if not all([token, owner, repo]):
        print("Skipping GitHub dispatch: Missing GITHUB_TOKEN, REPO_OWNER, or REPO_NAME.")
        return

    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "event_type": "platform-deploy",
        "client_payload": {
            "deployment_id": str(deployment.id),
            "cloud": deployment.cloud,
            "environment": deployment.environment,
            "application": deployment.application
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        print("DISPATCH STATUS:", response.status_code)
        print("DISPATCH BODY:", response.text)

        response.raise_for_status()
        print(f"GitHub pipeline triggered for deployment {deployment.id}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger GitHub pipeline: {e}")

    print("PAYLOAD:", payload)

