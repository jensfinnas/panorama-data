import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")

MURASAKI_USER = os.environ.get("MURASAKI_USER")
MURASAKI_PASSWORD = os.environ.get("MURASAKI_PASSWORD")

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

ENABLE_SLACK_NOTIFICATIONS = os.environ.get("ENABLE_SLACK_NOTIFICATIONS", True)