from google.cloud import secretmanager

PROJECT_ID = "satyanewproject-498206"
SECRET_ID = "jwt-secret"

client = secretmanager.SecretManagerServiceClient()

name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"

response = client.access_secret_version(
    request={"name": name}
)

secret = response.payload.data.decode("UTF-8")

print("Secret retrieved successfully")
print(secret)
