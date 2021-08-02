import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV")
class Config:
    if env == "development":
        environment = "DEV"
    elif env == "production":
        environment = "PROD"

    FLASK_APP = os.environ.get('FLASK_APP')
    host = os.getenv(f"{environment}_HOST")
    port = int(os.getenv(f"{environment}_PORT"))
    db_user = os.getenv(f"{environment}_DB_USER")
    db_password = os.getenv(f"{environment}_DB_PASSWORD")
    db_host = os.getenv(f"{environment}_DB_HOST")
    db_port = os.getenv(f"{environment}_DB_PORT")
    db_name = os.getenv(f"{environment}_DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
