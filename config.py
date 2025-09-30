import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ROUTER_IP = os.getenv("ROUTER_IP", "192.168.1.1")
    ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD", "admin")
    try:
        POLLING_INTERVAL_SECONDS = int(os.getenv("POLLING_INTERVAL_SECONDS", 60))
    except ValueError:
        POLLING_INTERVAL_SECONDS = 60 # Fallback to default if conversion fails
