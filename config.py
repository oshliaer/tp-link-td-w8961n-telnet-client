import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ROUTER_IP = os.getenv("ROUTER_IP", "192.168.1.1")
    ROUTER_USERNAME = os.getenv("ROUTER_USERNAME", "admin")
    ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD", "admin")
    POLLING_INTERVAL_SECONDS = int(os.getenv("POLLING_INTERVAL_SECONDS", 60))
