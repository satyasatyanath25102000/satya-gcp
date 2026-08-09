from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from google.cloud.sql.connector import (
    Connector,
    IPTypes,
)

from .config import get_app_secrets


# ==========================================
# Load secrets
# ==========================================

secrets = get_app_secrets()

DB_USER = secrets["DB_USER"]
DB_PASSWORD = secrets["DB_PASSWORD"]


# ==========================================
# Cloud SQL configuration
# ==========================================

DB_NAME = "jwt_demo"

INSTANCE_CONNECTION_NAME = (
    "satyanewproject-498206:us-central1:test"
)


# ==========================================
# Cloud SQL Connector
# ==========================================

connector = Connector()


def getconn():

    return connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        ip_type=IPTypes.PUBLIC,
    )


# ==========================================
# SQLAlchemy
# ==========================================

engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


# ==========================================
# FastAPI dependency
# ==========================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
