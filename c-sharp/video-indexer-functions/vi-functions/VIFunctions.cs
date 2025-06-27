using Azure.Core;
using Azure.Identity;
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
using vi_functions.models.vi_functions.models;
using Azure.Identity;
using Azure.Core;

namespace vi_functions;

/// <summary>
/// Contains Azure Functions that integrate with Azure Video Indexer to process,
/// index and retrieve information about video content.
/// </summary>
public class VIFunctions
{
    private readonly ILogger<VIFunctions> _logger;
    private readonly HttpClient _httpClient;
    private readonly CosmosClient _cosmosClient;
    private readonly string _dbName;
    private readonly string _containerName;

    /// <summary>
    /// Initializes a new instance of the VIFunctions class.
    /// </summary>
    /// <param name="logger">Logger for recording diagnostic information.</param>
    public VIFunctions(ILogger<VIFunctions> logger)
    {
        _logger = logger;
        _httpClient = new HttpClient();

        // Initialize Cosmos DB client using environment variables
        string cosmosEndpoint = Environment.GetEnvironmentVariable("CosmosDBEndpoint");
        string cosmosKey = Environment.GetEnvironmentVariable("CosmosDBKey");
        _dbName = Environment.GetEnvironmentVariable("CosmosDBName");
        _containerName = Environment.GetEnvironmentVariable("CosmosDBContainer");

        _cosmosClient = new CosmosClient(cosmosEndpoint, cosmosKey);
    }

    /// <summary>
    /// A simple heartbeat function to verify the service is operational.
    /// </summary>
    /// <param name="req">The HTTP request.</param>
    /// <returns>An OK response with a confirmation message.</returns>
    [Function("heartbeat")]
    public IActionResult Run([HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequest req)
    {
        _logger.LogInformation("C# Heartbeat function called.");
        return new OkObjectResult("We are here!\nWe are here!\nWe are here! \n\n\t- The Whos");
    }

    /// <summary>
    /// Retrieves the current processing status of a video from Video Indexer.
    /// </summary>
    /// <param name="req">The HTTP request.</param>
    /// <param name="fileName">Original file name of the video to get status for.</param>
    /// <returns>Status information about the requested video.</returns>
    [Function("GetVideoStatus")]
    public async Task<IActionResult> GetVideoStatus(
    [HttpTrigger(AuthorizationLevel.Function, "get", Route = "video-status/{fileName}")] HttpRequest req,
    string fileName)
    {
        _logger.LogInformation($"Getting video status for: {fileName}");

        try
        {
            // 1. Find the video in Cosmos DB by original file name
            var database = _cosmosClient.GetDatabase(_dbName);
            var container = database.GetContainer(_containerName);

            // Query to find the video by original file name
            var query = new QueryDefinition("SELECT * FROM c WHERE c.OriginalFileName = @fileName")
                .WithParameter("@fileName", fileName);

            var videoResults = new List<VideoIndexerResult>();
            using (var iterator = container.GetItemQueryIterator<VideoIndexerResult>(query))
            {
                while (iterator.HasMoreResults)
                {
                    var response = await iterator.ReadNextAsync();
                    videoResults.AddRange(response);
                }
            }

            if (!videoResults.Any())
            {
                _logger.LogWarning($"No video found with file name: {fileName}");
                return new NotFoundObjectResult($"No video found with file name: {fileName}");
            }

            // Use the first result if multiple are found
            var videoInfo = videoResults.Last();
            _logger.LogInformation($"Found video in database. Video ID: {videoInfo.Id}");

            // 2. Get video indexer access token
            string location = Environment.GetEnvironmentVariable("VideoIndexerLocation");
            string accountId = videoInfo.AccountId ?? Environment.GetEnvironmentVariable("VideoIndexerAccountId");
            string accessToken = await GetVideoIndexerAccessToken();

            // 3. Call Video Indexer API to get current status
            var videoStatus = await GetVideoIndexStatus(location, accountId, videoInfo.Id, accessToken);

            // 4. Return the results
            return new OkObjectResult(videoStatus);
        }
        catch (Exception ex)
        {
            _logger.LogError($"Error retrieving video status: {ex.Message}");
            return new StatusCodeResult(StatusCodes.Status500InternalServerError);
        }
    }

    /// <summary>
    /// Retrieves basic indexing status information for a video from Video Indexer API.
    /// </summary>
    /// <param name="location">Video Indexer region/location.</param>
    /// <param name="accountId">Video Indexer account ID.</param>
    /// <param name="videoId">ID of the video in Video Indexer.</param>
    /// <param name="accessToken">Access token for Video Indexer API.</param>
    /// <returns>A simplified object containing video status information.</returns>
    private async Task<object> GetVideoIndexStatus(string location, string accountId, string videoId, string accessToken)
    {
        _logger.LogInformation($"Getting video index status for video ID: {videoId}");

        var requestUrl = $"https://api.videoindexer.ai/{location}/Accounts/{accountId}/Videos/{videoId}/Index";

        // Build request URL with query parameters
        var requestUri = new UriBuilder(requestUrl);
        var query = System.Web.HttpUtility.ParseQueryString(string.Empty);
        query["accessToken"] = accessToken;
        // Include only what we need to reduce response size
        query["includedInsights"] = "Transcript";
        query["includeSummarizedInsights"] = "false";
        requestUri.Query = query.ToString();

        // Configure and send request
        var request = new HttpRequestMessage(HttpMethod.Get, requestUri.Uri);
        request.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogError($"Video Indexer API error: {response.StatusCode} - {content}");
            throw new Exception($"Video Indexer API error: {response.StatusCode}");
        }

        // Parse the response
        var videoDetails = JsonConvert.DeserializeObject<VideoIndexResponse>(content);

        // Create a simplified response with only relevant information
        var result = new
        {
            Id = videoId,
            Name = videoDetails.Name,
            State = videoDetails.State,
            ProcessingProgress = videoDetails.Videos?[0]?.ProcessingProgress,
            Duration = videoDetails.DurationInSeconds,
            CreatedDate = videoDetails.Created,
            FailureMessage = videoDetails.Videos?[0]?.FailureMessage
        };

        return result;
    }

    /// <summary>
    /// Retrieves detailed indexing information for a video from Video Indexer.
    /// </summary>
    /// <param name="req">The HTTP request.</param>
    /// <param name="fileName">Original file name of the video to get details for.</param>
    /// <returns>Detailed indexing information from Video Indexer.</returns>
    [Function("GetVideoIndexingDetails")]
    public async Task<IActionResult> GetVideoIndexingDetails(
    [HttpTrigger(AuthorizationLevel.Function, "get", Route = "video-indexing/{fileName}")] HttpRequest req,
    string fileName)
    {
        _logger.LogInformation($"Getting video indexing details for: {fileName}");

        try
        {
            // 1. Find the video in Cosmos DB by original file name
            var database = _cosmosClient.GetDatabase(_dbName);
            var container = database.GetContainer(_containerName);

            // Query to find the video by original file name
            var query = new QueryDefinition("SELECT * FROM c WHERE c.OriginalFileName = @fileName")
                .WithParameter("@fileName", fileName);

            var videoResults = new List<VideoIndexerResult>();
            using (var iterator = container.GetItemQueryIterator<VideoIndexerResult>(query))
            {
                while (iterator.HasMoreResults)
                {
                    var response = await iterator.ReadNextAsync();
                    videoResults.AddRange(response);
                }
            }

            if (videoResults.Count == 0)
            {
                _logger.LogWarning($"No video found with file name: {fileName}");
                return new NotFoundObjectResult($"No video found with file name: {fileName}");
            }

            // Use the first result if multiple are found
            var videoInfo = videoResults.First();
            _logger.LogInformation($"Found video in database. Video ID: {videoInfo.Id}");

            // 2. Get video indexer access token
            string location = Environment.GetEnvironmentVariable("VideoIndexerLocation");
            string accountId = videoInfo.AccountId ?? Environment.GetEnvironmentVariable("VideoIndexerAccountId");
            string accessToken = await GetVideoIndexerAccessToken();

            // 3. Call Video Indexer API to get detailed index information
            var videoIndexDetails = await GetDetailedVideoIndex(location, accountId, videoInfo.Id, accessToken);

            // 4. Return the results
            return new OkObjectResult(videoIndexDetails);
        }
        catch (Exception ex)
        {
            _logger.LogError($"Error retrieving video indexing details: {ex.Message}");
            return new StatusCodeResult(StatusCodes.Status500InternalServerError);
        }
    }

    /// <summary>
    /// Retrieves comprehensive video indexing details from Video Indexer API.
    /// </summary>
    /// <param name="location">Video Indexer region/location.</param>
    /// <param name="accountId">Video Indexer account ID.</param>
    /// <param name="videoId">ID of the video in Video Indexer.</param>
    /// <param name="accessToken">Access token for Video Indexer API.</param>
    /// <returns>A structured object containing detailed indexing information.</returns>
    private async Task<object> GetDetailedVideoIndex(string location, string accountId, string videoId, string accessToken)
    {
        _logger.LogInformation($"Getting detailed video index for video ID: {videoId}");

        var requestUrl = $"https://api.videoindexer.ai/{location}/Accounts/{accountId}/Videos/{videoId}/Index";

        // Build request URL with query parameters
        var requestUri = new UriBuilder(requestUrl);
        var query = System.Web.HttpUtility.ParseQueryString(string.Empty);
        query["accessToken"] = accessToken;

        // Include specific insights based on requirements
        // Can be customized to include specific insights: "Transcript,Faces,Labels,Sentiments" etc.
        query["includedInsights"] = "Transcript,Sentiments,Keywords,Faces,Labels,Brands,Emotions";
        query["includeSummarizedInsights"] = "true";
        requestUri.Query = query.ToString();

        // Configure and send request
        var request = new HttpRequestMessage(HttpMethod.Get, requestUri.Uri);
        request.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogError($"Video Indexer API error: {response.StatusCode} - {content}");
            throw new Exception($"Video Indexer API error: {response.StatusCode}");
        }

        // Parse the response
        // Parse the response using the strongly-typed VideoIndexResponse model
        var videoDetails = JsonConvert.DeserializeObject<VideoIndexResponse>(content);

        if (videoDetails == null)
        {
            throw new Exception("Failed to parse Video Indexer API response");
        }

        // Return the full video details object instead of creating a new anonymous object
        return videoDetails;
    }

    /// <summary>
    /// Azure Function triggered when a new video blob is added to the storage container.
    /// Processes the video by sending it to Video Indexer and storing metadata in Cosmos DB.
    /// </summary>
    /// <param name="blobStream">Stream containing the video blob content.</param>
    /// <param name="name">Name of the blob that triggered the function.</param>
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
            string accessToken = await GetVideoIndexerAccessToken();

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

    /// <summary>
    /// Generates a SAS URL for a blob to provide temporary access for Video Indexer.
    /// </summary>
    /// <param name="blobName">Name of the blob to generate SAS URL for.</param>
    /// <returns>SAS URL for the blob.</returns>
    /// <remarks>
    /// This is a placeholder implementation. In production, you should generate
    /// an actual SAS token with appropriate permissions and expiration time.
    /// </remarks>
    private string GenerateBlobSasUrl(string blobName)
    {
        // In a real implementation, you would generate a SAS URL for the blob
        // For simplicity, we'll assume the URL is available in an environment variable or constructed
        string storageAccountUrl = Environment.GetEnvironmentVariable("StorageAccountUrl");
        string container = Environment.GetEnvironmentVariable("StorageContainer");

        // This is a placeholder - in production, you would generate a proper SAS URL
        return $"{storageAccountUrl}/{container}/{blobName}";
    }

    /// <summary>
    /// Uploads a video to Azure Video Indexer for processing.
    /// </summary>
    /// <param name="location">Video Indexer region/location.</param>
    /// <param name="accountId">Video Indexer account ID.</param>
    /// <param name="accessToken">Access token for Video Indexer API.</param>
    /// <param name="videoName">Name to assign to the video in Video Indexer.</param>
    /// <param name="videoUrl">Public URL where the video can be accessed.</param>
    /// <returns>Video indexer result containing metadata about the uploaded video.</returns>
    private async Task<VideoIndexerResult> UploadToVideoIndexer(string location, string accountId, string accessToken, string videoName, string videoUrl)
    {
        var requestUrl = $"https://api.videoindexer.ai/{location}/Accounts/{accountId}/Videos";

        // Build request URL with query parameters
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

    /// <summary>
    /// Stores video indexing metadata in Cosmos DB for later retrieval.
    /// </summary>
    /// <param name="videoData">Video indexer result to store.</param>
    /// <param name="originalFileName">Original file name of the video.</param>
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

    /// <summary>
    /// Retrieves an access token for the Video Indexer API using managed identity authentication.
    /// </summary>
    /// <returns>Access token for Video Indexer API calls.</returns>
    private async Task<string> GetVideoIndexerAccessToken()
    {
        try
        {
            _logger.LogInformation("Getting Video Indexer access token using managed identity");

            // First, get an Azure AD token using the managed identity
            var tokenProvider = new DefaultAzureCredential();
            var azureAdToken = await tokenProvider.GetTokenAsync(
                new TokenRequestContext(new[] { "https://management.azure.com/.default" }));

            // Now use that token to get a Video Indexer access token
            var viTokenUrl = $"https://management.azure.com/subscriptions/{Environment.GetEnvironmentVariable("SubscriptionId")}/resourceGroups/{Environment.GetEnvironmentVariable("ResourceGroupName")}/providers/Microsoft.VideoIndexer/accounts/{Environment.GetEnvironmentVariable("VideoIndexerAccountName")}/generateAccessToken?api-version=2025-04-01";

            var request = new HttpRequestMessage(HttpMethod.Post, viTokenUrl);
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", azureAdToken.Token);

            // Request body to specify the permissions
            var requestBody = new
            {
                permissionType = "Contributor",
                scope = "Account"
            };
            request.Content = new StringContent(
                JsonConvert.SerializeObject(requestBody),
                System.Text.Encoding.UTF8,
                "application/json");

            var response = await _httpClient.SendAsync(request);
            var content = await response.Content.ReadAsStringAsync();

            if (!response.IsSuccessStatusCode)
            {
                _logger.LogError($"Failed to get Video Indexer token: {response.StatusCode} - {content}");
                throw new Exception($"Failed to get Video Indexer token: {response.StatusCode}");
            }

            var tokenResponse = JsonConvert.DeserializeObject<VideoIndexerTokenResponse>(content);
            return tokenResponse.AccessToken;
        }
        catch (Exception ex)
        {
            _logger.LogError($"Error getting Video Indexer access token: {ex.Message}");
            throw;
        }
    }
}