import os

EMAIL_ALERTS = os.getenv("EMAIL_ALERTS", "false").lower() == "true"
SLACK_ALERTS = os.getenv("SLACK_ALERTS", "false").lower() == "true"


