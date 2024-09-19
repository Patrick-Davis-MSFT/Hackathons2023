# Sample App with Semantic Kernel With Plug-ins

This simple app is a console C# app created to illustrate how to use several plugins with semantic kernel. 

For more information on Semantic Kernel please see the [Microsoft Learn Documentation](https://learn.microsoft.com/en-us/semantic-kernel/overview/)

> *Note*: This sample not intended for enterprise use.

## Required Dependencies 
### Local Console Program
* .NET 8 (Visual Studio)
* Microsoft.Azure.Search
* Microsoft.Extensions.Logging
* Microsoft.SemanticKernel
* Azure.Search.Documents

### Azure Resources
* Azure Open AI with a Chat Deployment and a GPT-4 Deployment with vision and an ADA model deployment
* Azure Storage Account
* Azure AI Search with Semantic Ranker turned on
    * Use the Azure AI Search "Import and Vectorize Data" to populate an index

The Azure AI Search System Managed Identity needs to have the following role assignments
* *Storage Blob Data Reader* on the Storage Account and the Blob Storage Container
* *Cognitive Services User* on the Azure OpenAI service
* *Cognitive Services OpenAI User* on the Azure OpenAI service

## Settings file
The settings files is the configuration for all endpoints
1. Copy `settings.example.json` to `settings.json`
1. The folloing settings are required

|Setting|Description|
|deploymentId|The deployment for the user and agent chat.|
|endpoint|The endpoint for the user and agent chat. End with a `/` do not include the `/openai/` path.|
|apiKey|The api key for the user and agent chat.|
|searchIndexName|Index name for Azure AI Search|
|searchEndpoint|Azure AI Search Endpoint|
|searchQueryApiKey|Azure AI Search API Key|
|visionDeploymentModel|The deployment for the gpt-4 vision integration.|
|visionApiKey|The endpoint for the gpt-4 vision integration. End with a `/` do not include the `/openai/` path.|
|apiKey|The api key for the gpt-4 vision integration.|
|visionAPIVersion|The api version for the gpt-4 vision integration. See [Azure OpenAI API version documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference) for the latest versions.|

## Optional Plug in Azure API Management

### Required Resources
* Log Analytics 
* Applicaiton Insights
* Azure API Management in the Developer SKU

> Note this was tested with the API version 2024-08-01-preview Azure OpenAI API

1. Give the system managed identity the following roles
    * *Cognitive Services User* on the Azure OpenAI service
    * *Cognitive Services OpenAI User* on the Azure OpenAI service
1. Create the following named values
    * create a named value for the Azure AI Search Key called `azure-ai-search-key`
1. Create a new API for the Azure AI Search
    1. Web URL set to the Azure AI Search
    1. API URL Suffix `aisearch`
    1. Set the products as appropriately.
    1. Set Subscription Required and set the Header Name under Subscription should be `api-key`
    1. Create 2 operations 
        1. Method GET set the URL to /* and the Method to GET
        1. Method POST set the URL to /* and the Method to POST
    1. Apply the policy in the `apim-setup/apim-policy` to the azure-ai-search policy
    1. Update the searchEndpoint in the settings file with the Base URL on the Settings page
    1. Update the searchQueryApiKey to the subscription key
1. Create a new API for the Azure OpenAI 
    1. Create a new OpenAPI with the specification in the `apim-setup/openAPI-spec` folder
    1. Apply the policy in the `apim-setup/apim-policy` to the azure open ai
    1. Set the Subscription Header Name to `api-key`
    1. Ensure that the API URL suffix ends with `/openai`
    1. Set the products as appropriately.
    1. Update the OpenAI endpoints in the settings.json file to the Base URL without the `openai` at the end
    1. Update the OpenAI api-key in the settings.json to the subscription key