using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using vi_functions.models;

namespace vi_functions;

public class VIFunctions
{
    private readonly ILogger<VIFunctions> _logger;
    private readonly HttpClient _httpClient;
    private readonly CosmosClient _cosmosClient;
    private readonly string _dbName;
    private readonly string _containerName;

    public VIFunctions(ILogger<VIFunctions> logger)
    {
        _logger = logger;
        _httpClient = new HttpClient();

        // Initialize Cosmos DB client
        string cosmosEndpoint = Environment.GetEnvironmentVariable("CosmosDBEndpoint");
        string cosmosKey = Environment.GetEnvironmentVariable("CosmosDBKey");
        _dbName = Environment.GetEnvironmentVariable("CosmosDBName");
        _containerName = Environment.GetEnvironmentVariable("CosmosDBContainer");

        _cosmosClient = new CosmosClient(cosmosEndpoint, cosmosKey);
    }

    [Function("heartbeat")]
    public IActionResult Run([HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequest req)
    {
        _logger.LogInformation("C# Heartbeat function called.");
        return new OkObjectResult("We are here!\nWe are here!\nWe are here! \n\n\t- The Whos");
    }

    [Function("ProcessNewVideo")]
    public async Task RunAsync(
           [Microsoft.Azure.Functions.Worker.BlobTrigger("%StorageContainer%/{name}", Connection = "StorageConnection")] Stream blobStream,
           string name)
    {
        _logger.LogInformation($"Processing new video blob: {name}");

        try
        {
            // Get Video Indexer settings from environment variables
            string location = Environment.GetEnvironmentVariable("VideoIndexerLocation");
            string accountId = Environment.GetEnvironmentVariable("VideoIndexerAccountId");
            string accessToken = Environment.GetEnvironmentVariable("VideoIndexerAccessToken");

            // Generate a SAS URL for the blob if needed
            string videoUrl = GenerateBlobSasUrl(name);

            // Upload to Video Indexer
            var videoData = await UploadToVideoIndexer(location, accountId, accessToken, name, videoUrl);

            // Store result in Cosmos DB
            await StoreVideoDataInCosmosDb(videoData, name);

            _logger.LogInformation($"Video {name} processed successfully. Video ID: {videoData.Id}");
        }
        catch (Exception ex)
        {
            _logger.LogError($"Error processing video {name}: {ex.Message}");
            throw;
        }
    }

    private string GenerateBlobSasUrl(string blobName)
    {
        // In a real implementation, you would generate a SAS URL for the blob
        // For simplicity, we'll assume the URL is available in an environment variable or constructed
        string storageAccountUrl = Environment.GetEnvironmentVariable("StorageAccountUrl");
        string container = Environment.GetEnvironmentVariable("StorageContainer");

        // This is a placeholder - in production, you would generate a proper SAS URL
        return $"{storageAccountUrl}/{container}/{blobName}";
    }

    private async Task<VideoIndexerResult> UploadToVideoIndexer(string location, string accountId, string accessToken, string videoName, string videoUrl)
    {
        var requestUrl = $"https://api.videoindexer.ai/{location}/Accounts/{accountId}/Videos";

        var requestUri = new UriBuilder(requestUrl);
        var query = System.Web.HttpUtility.ParseQueryString(string.Empty);

        // Set required parameters
        query["name"] = videoName;
        query["privacy"] = "Private";
        query["videoUrl"] = videoUrl;
        query["accessToken"] = accessToken;

        // Optional parameters from environment variables if specified
        string language = Environment.GetEnvironmentVariable("VideoIndexerLanguage");
        if (!string.IsNullOrEmpty(language))
            query["language"] = language;

        string indexingPreset = Environment.GetEnvironmentVariable("VideoIndexerPreset");
        if (!string.IsNullOrEmpty(indexingPreset))
            query["indexingPreset"] = indexingPreset;

        requestUri.Query = query.ToString();

        // Make the API call
        _logger.LogInformation($"Making Video Indexer API call to: {requestUri.Uri}");

        var request = new HttpRequestMessage(HttpMethod.Post, requestUri.Uri);
        request.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogError($"Video Indexer API error: {response.StatusCode} - {content}");
            throw new Exception($"Video Indexer API error: {response.StatusCode}");
        }

        // Deserialize the response
        return JsonConvert.DeserializeObject<VideoIndexerResult>(content);
    }

    private async Task StoreVideoDataInCosmosDb(VideoIndexerResult videoData, string originalFileName)
    {
        try
        {
            var database = _cosmosClient.GetDatabase(_dbName);
            var container = database.GetContainer(_containerName);

            // Add additional metadata
            videoData.OriginalFileName = originalFileName;
            videoData.ProcessedDate = DateTime.UtcNow;

            // Store in Cosmos DB
            await container.CreateItemAsync(videoData, new PartitionKey(videoData.Name));

            _logger.LogInformation($"Video data stored in Cosmos DB successfully: {videoData.Id}");
        }
        catch (Exception ex)
        {
            _logger.LogError($"Error storing video data in Cosmos DB: {ex.Message}");
            throw;
        }
    }

}