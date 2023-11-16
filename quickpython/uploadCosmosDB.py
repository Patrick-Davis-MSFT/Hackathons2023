# to run 
# import requirements
# pip install -r ./requirements.txt
# run the command
# python .\uploadCosmosDB.py -d <database name> -c <container name> -e <endpoint> -k <key> -n <item value>
# Hint: an indexer on cognitive search can be setup to automatically index the data in the Cosmos DB


import json
import os
import sys
import uuid
import argparse
from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey




if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Convert PDF to text. Output appends to existing file, so if you want to start fresh, delete the output file')
    parser.add_argument('-d', '--dbname', help='cosmos db name', required=True)
    parser.add_argument('-c', '--containername', help='cosmos container name', required=True)
    parser.add_argument('-e', '--endpoint', help='cosmos endpoint', required=True)
    parser.add_argument('-k', '--key', help='cosmos access key', required=True)
    parser.add_argument('-n', '--itemvalue', help='item value for upsert', required=True)
    
    parser.add_argument('-i', '--itemid', help='item id for upsert', required=False)
    args = parser.parse_args()
    # Set up the connection to Azure Cosmos DB
    url = args.endpoint
    credential = args.key
    client = CosmosClient(url, credential)

    # Create a database and container
    database_name = args.dbname
    container_name = args.containername
    id = args.itemid or str(uuid.uuid4())
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path='/id'),
        offer_throughput=400
    )

    # Insert data into the container
    data = {'id': id, 'name': args.itemvalue}
    container.upsert_item(body=data)