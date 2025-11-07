import os
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
load_dotenv()

ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER")
CLIENT_ID = os.getenv("AZURE_STORAGE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_STORAGE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_STORAGE_TENANT_ID")

def get_blob_service():
    cred = ClientSecretCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return BlobServiceClient(account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net", credential=cred)

def upload_to_adls(local_path, blob_name):
    blob_service = get_blob_service()
    container_client = blob_service.get_container_client(CONTAINER_NAME)
    with open(local_path, "rb") as f:
        container_client.upload_blob(name=blob_name, data=f, overwrite=True)
    return f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
