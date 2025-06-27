# Video Indexer Example C#

Resources needed for Video Indexer functions to operate
* Cosmos DB (standard, non-georeplicated)
    * DB Name: vindxr
    * Container Name: video
* Managed Identity
    * Permissions (set at the resource group or lower)
        * Storage Blob Data Owner
        * Monitoring Metrics Publisher
        * Cognitive Services Contributor
        * Cognitive Services OpenAI Contributor
* Video Indexer
    * Use the managed identity created above
* Storage Account 
    * Blob Container Name: videoin 
* Function App
    * .NET 8 Isolated
    * Identity set to the managed identity

Deploy the included project with the approprate variables to the function app
