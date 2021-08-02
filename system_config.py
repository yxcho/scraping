import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("ENV") == "development":
    env = "DEV"
elif os.getenv("ENV") == "production":
    env = "PROD"


host = os.getenv(f"{env}_HOST")
port = os.getenv(f"{env}_PORT")