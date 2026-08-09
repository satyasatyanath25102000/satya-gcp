import json

from google.cloud import secretmanager


PROJECT_ID = "satyanewproject-498206"
SECRET_ID = "app-secrets"


def get_app_secrets() -> dict:

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
print(get_app_secrets())
