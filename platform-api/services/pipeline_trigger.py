from threading import Thread
from services.github_dispatch import trigger_github_pipeline


def trigger_pipeline(deployment):
    Thread(
        target=trigger_github_pipeline,
        args=(deployment,),
        daemon=True
    ).start()