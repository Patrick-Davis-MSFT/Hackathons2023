// Import packages
using chat_app.plugins;
using chat_app.config;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using static System.Net.WebRequestMethods;
using Azure.AI.OpenAI.Chat;


Settings settings = new Settings();

static AzureSearchChatDataSource GetAzureSearchDataSource(string searchIndexName, string searchQueryApiKey, string searchEndpoint)
{
    return new AzureSearchChatDataSource
    {
        Endpoint = new Uri(searchEndpoint),
        Authentication = DataSourceAuthentication.FromApiKey(searchQueryApiKey),
        IndexName = searchIndexName
    };
}

// Create a kernel with Azure OpenAI chat completion
var builder = Kernel.CreateBuilder().AddAzureOpenAIChatCompletion(settings.config.deploymentId, settings.config.endpoint, settings.config.apiKey);

// Build the kernel
Kernel kernel = builder.Build();
var chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

var campingPlugin = new AzureAISearchPlugin(settings.config.searchIndexName, settings.config.searchQueryApiKey, settings.config.searchEndpoint);
var imagePlugin = new ImagePlugin(settings.config.visionDeploymentModel,settings.config.visionApiKey,settings.config.visionEndpoint,settings.config.visionAPIVersion);

// Add a plugin (the LightsPlugin class is defined below)
kernel.Plugins.AddFromType<LightsPlugin>("Lights");
kernel.Plugins.AddFromType<WeatherPlugin>("Weather");
kernel.Plugins.AddFromObject(campingPlugin, "CampingInfoSearch");
kernel.Plugins.AddFromObject(imagePlugin, "ImageDescription");

// set the data source for the document 
var dataSource = GetAzureSearchDataSource(settings.config.searchIndexName, settings.config.searchQueryApiKey, settings.config.searchEndpoint);

// Enable planning
OpenAIPromptExecutionSettings openAIPromptExecutionSettings = new()
{
    ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions
};

// Create a history store the conversation
var history = new ChatHistory();

// Initiate a back-and-forth chat
string? userInput;
history.AddMessage(AuthorRole.System, "Your name is Azure Andy and you are an AI assistant. Help the user in their requests");
do
{
    // Collect user input
    Console.Write("User > ");
    userInput = Console.ReadLine();

    // Add user input
    history.AddUserMessage(userInput);

    // Get the response from the AI
    var result = await chatCompletionService.GetChatMessageContentAsync(
        history,
        executionSettings: openAIPromptExecutionSettings,
        kernel: kernel);

    // Print the results
    Console.WriteLine("Assistant > " + result);

    // Add the message from the agent to the chat history
    history.AddMessage(result.Role, result.Content ?? string.Empty);
} while (userInput is not null);