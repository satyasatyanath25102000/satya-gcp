import json

from google.cloud import secretmanager
from google.cloud.sql.connector import Connector, IPTypes

from sqlalchemy import create_engine, text


# ==============================
# GCP configuration
# ==============================

PROJECT_ID = "satyanewproject-498206"
SECRET_ID = "app-secrets"

INSTANCE_CONNECTION_NAME = (
    "satyanewproject-498206:us-central1:test"
)

DB_NAME = "jwt_demo"


# ==============================
# Get secrets from Secret Manager
# ==============================

def get_app_secrets():

    client = secretmanager.SecretManagerServiceClient()

    name = (
        f"projects/{PROJECT_ID}"
        f"/secrets/{SECRET_ID}"
        f"/versions/latest"
    )

    response = client.access_secret_version(
        request={"name": name}
    )

    secret_value = response.payload.data.decode("UTF-8")

    return json.loads(secret_value)


# ==============================
# Load credentials
# ==============================

secrets = get_app_secrets()

DB_USER = secrets["DB_USER"]
DB_PASSWORD = secrets["DB_PASSWORD"]


# ==============================
# Cloud SQL Connector
# ==============================

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


# ==============================
# SQLAlchemy
# ==============================

engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn,
    pool_pre_ping=True,
)


# ==============================
# Test connectivity
# ==============================

try:

    with engine.connect() as connection:

        result = connection.execute(
            text(
                """
                SELECT
                    current_database(),
                    current_user,
                    version()
                """
            )
        )

        row = result.fetchone()

        print("Database:", row[0])
        print("User:", row[1])
        print("PostgreSQL:", row[2])
        print()
        print("Database connectivity successful!")


except Exception as e:

    print("Database connection failed:")
    print(type(e).__name__)
    print(e)


finally:

    connector.close()
