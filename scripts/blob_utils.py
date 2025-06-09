from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

def upload_file_to_blob(local_path, blob_name, connection_string=CONNECTION_STRING, container_name=CONTAINER_NAME):
    """
    Upload a local file to Azure Blob Storage.
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(local_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {local_path} to blob {blob_name}")

def download_blob_to_file(blob_name, local_path, connection_string=CONNECTION_STRING, container_name=CONTAINER_NAME):
    """
    Download a blob from Azure Blob Storage to a local file.
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(local_path, "wb") as data:
        data.write(blob_client.download_blob().readall())
    print(f"Downloaded blob {blob_name} to {local_path}")