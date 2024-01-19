# MIT License

# To run this place quotes around all the parameters
# python ./removeInfoAssistFile.py -f <filename> -d <folder> -b <blobConnectString> -s <searchEndPoint> -k <searchKey> -ce <cosmosEndpoint> -ck <cosmosKey>


# The required libraries have been added to the requirements.txt file
# pip install -r ./requirements.txt

# using the set command it will only set the variables during the current console session and will not persist.

from azure.core.credentials import AzureKeyCredential
import argparse
import base64
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.cosmos import CosmosClient, PartitionKey
from rich.console import Console
import rich.traceback

rich.traceback.install()
console = Console()

UPLOAD_CONTAINER_NAME = "upload"
OUTPUT_CONTAINER_NAME = "content"
STATUS_CONTAINER_NAME = "statuscontainer"
STATUS_DB_NAME = "statusdb"
INDEX_NAME= "vector-index"

def encode_document_id(document_id):
    """ encode a path/file name to remove unsafe chars for a cosmos db id """
    safe_id = base64.urlsafe_b64encode(document_id.encode()).decode()
    return safe_id

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Remove a file out of info assist.')
    
    parser.add_argument('-f', '--filename', help='File Name to Delete', required=True)
    parser.add_argument('-d', '--folder', help='Folder Name the file is loaded to', required=False)
    parser.add_argument('-b', '--blobConnectString', help='Blob ConnectionString', required=True)
    parser.add_argument('-s', '--searchEndPoint', help='Search Service End Point',  required=True)
    parser.add_argument('-k', '--searchKey', help='Search Service End Point',  required=True)
    parser.add_argument('-ce', '--cosmosEndpoint', help='cosmos endpoint', required=True)
    parser.add_argument('-ck', '--cosmosKey', help='cosmos access key', required=True)
    args = parser.parse_args()
    console.print("Cleaning up Files...")
    filename = args.filename
    folder = args.folder + "/" or ""
    blobConnectString = args.blobConnectString
    searchEndPoint = args.searchEndPoint
    searchKey = args.searchKey
    storage_blob_service_client = BlobServiceClient.from_connection_string(blobConnectString)
    
    upload_container_client = storage_blob_service_client.get_container_client(UPLOAD_CONTAINER_NAME)
    output_container_client = storage_blob_service_client.get_container_client(OUTPUT_CONTAINER_NAME)
    azure_search_key_credential = AzureKeyCredential(searchKey)
    search_client = SearchClient(
        endpoint=searchEndPoint,
        index_name=INDEX_NAME,
        credential=azure_search_key_credential,
    )

        # Cleanup upload container
    try:
        console.print(f"Deleting blob: {folder}{filename}")
        upload_container_client.delete_blob(f'{folder}{filename}')
    except Exception as ex:
        console.print(f"Failed to delete blob: {folder}{filename}. Error: {ex}")

    # Remove filename extension
    extensionPlace = filename.rfind('.')
    if extensionPlace > 1:
        filenameNew = filename[:extensionPlace-1]
    else:
        filenameNew = filename
    console.print(f"Searching For File: {filenameNew}")
    # Cleanup output container
    blobs = output_container_client.list_blobs(name_starts_with=f"{folder}{filenameNew}")
    for blob in blobs:
        console.print(f"Deleting blob: {blob.name}")
        try:
            output_container_client.delete_blob(blob.name)
            console.print(f"Deleted blob: {blob.name}")
        except Exception as ex:
            console.print(f"Failed to delete blob: {blob.name}. Error: {ex}")

        console.print(f"Deleting Index Entry: {blob.name}")
        try:
            # Cleanup search index
            console.print(f"Removing document from index: {blob.name} \
                          : id : {encode_document_id(blob.name)}")
            search_client.delete_documents(documents=[{"id": f"{encode_document_id(blob.name)}"}])
        except Exception as ex:
            console.print(f"Failed to remove document from index: {blob.name} \
                          : id : {encode_document_id(blob.name)}. Error: {ex}")

    #Cleanup File Load History
    console.print(f"Removing document from Cosmos DB: {filename}")
    url = args.cosmosEndpoint
    credential = args.cosmosKey
    client = CosmosClient(url, credential)
    database_name = STATUS_DB_NAME
    container_name = STATUS_CONTAINER_NAME
    id = filename
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    query = "SELECT * FROM c where c.file_name = @file"
    parameters = [{"name": "@file", "value": filename}]
    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    if len(items) == 0:
        console.print(f"Document not found in Cosmos DB: {filename}")
    for item in items:
        console.print(f"Removing document from Cosmos DB: {item['file_path']}")
        container.delete_item(item, partition_key=item['file_name'])

    console.print("Finished cleaning up files.")