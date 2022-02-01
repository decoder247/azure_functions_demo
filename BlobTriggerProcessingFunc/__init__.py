import logging
import os
import uuid
from os.path import dirname, join, exists, split

import azure.functions as func
from azure.storage.blob import (
    BlobClient,
    BlobServiceClient,
    ContainerClient,
    __version__,
)
from dotenv import load_dotenv

# Load env variables
dotenv_path = join(dirname(dirname(__file__)), ".local", "credentials.env")
assert exists(dotenv_path), f"Credentials file - {dotenv_path} does not exist!"
load_dotenv(dotenv_path)


def get_url(account_name: str, source_container_name: str, source_file_path: str):
    return f"https://{account_name}.blob.core.windows.net/{source_container_name}/{source_file_path}"


def main(myblob: func.InputStream):
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    account_name = os.getenv("ACCOUNT_NAME")
    container_name = os.getenv("CONTAINER_NAME")

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=connect_str
    )  # ,container_name="demo"

    # # Create a unique name for the container and create container
    # container_name = str(uuid.uuid4())
    # container_client = blob_service_client.create_container(container_name)

    # Instantiate a new ContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    blob_list = container_client.list_blobs()
    for blob in blob_list:
        logging.info(f"\tBlob object name -> {blob.name}")
        logging.info(
            f"\tBlob object url -> {get_url(account_name,container_name,blob)}"
        )

    blob_url_to_copy = get_url(
        account_name, container_name.split("/")[0], myblob.name.split("/")[-1]
    )
    target_container_name = 'output'
    target_file_path = "target.txt"
    copied_blob = blob_service_client.get_blob_client(
        target_container_name, target_file_path
    )
    copied_blob.start_copy_from_url(blob_url_to_copy)

    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Methods: {myblob.__dict__}\n"
        f"URI: {myblob.uri}\n"
        f"Name: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes"
    )
