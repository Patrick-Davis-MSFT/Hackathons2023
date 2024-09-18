using Azure.Search.Documents.Models;
using Microsoft.SemanticKernel;
using System.ComponentModel;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.ChatCompletion;
using static System.Runtime.InteropServices.JavaScript.JSType;
using System.Text.Json;

namespace chat_app.plugins
{
    internal class ImagePlugin
    {
        internal string visionDeploymentModel { get; set; }
        internal string visionApiKey { get; set; }
        internal string visionEndpoint { get; set; }
        internal string visionAPIVersion { get; set; }
        private static string imageSystemPrompt = "You a are an assistant that describes images for vision impared users.";

        internal ImagePlugin(string visionDeploymentModel, string visionApiKey, string visionEndpoint, string visionAPIVersion)
        {
            this.visionDeploymentModel = visionDeploymentModel;
            this.visionApiKey = visionApiKey;
            this.visionEndpoint = visionEndpoint;
            this.visionAPIVersion = visionAPIVersion;
        }
        public static string LocalImageToDataUrl(string imagePath)
        {
            // Guess the MIME type of the image based on the file extension
            string mimeType = GetMimeType(imagePath);
            if (mimeType == null)
            {
                mimeType = "application/octet-stream"; // Default MIME type if none is found
            }

            // Read and encode the image file
            byte[] imageBytes = File.ReadAllBytes(imagePath);
            string base64EncodedData = Convert.ToBase64String(imageBytes);

            // Construct the data URL
            return $"data:{mimeType};base64,{base64EncodedData}";
        }

        private static string GetMimeType(string filePath)
        {
            string extension = Path.GetExtension(filePath).ToLowerInvariant();
            switch (extension)
            {
                case ".jpg":
                case ".jpeg":
                    return "image/jpeg";
                case ".png":
                    return "image/png";
                case ".gif":
                    return "image/gif";
                case ".bmp":
                    return "image/bmp";
                case ".tiff":
                    return "image/tiff";
                case ".ico":
                    return "image/x-icon";
                default:
                    return null;
            }
        }

        private static readonly HttpClient client = new HttpClient();

        [KernelFunction("imageDescription")]
        [Description("This function will decribe an image based on an input of an image file path")]
        [return: Description("Returns a description of an image based on a local file path")]
        public async Task<string> GetImageDescription(string filePath)
        {
            try
            {
                string dataUrl = LocalImageToDataUrl(filePath);
                //build message content
                string messageContent = $"{{\"messages\": [{{\"role\": \"system\",\"content\": \"{imageSystemPrompt}\"}},{{\"role\": \"user\", \"content\": [{{\"type\": \"text\",\"text\": \"Describe this picture:\"}},{{\"type\": \"image_url\",\"image_url\": {{\"url\": \"{dataUrl}\"}}}}]}}],\"max_tokens\": 1000,\"stream\": false}}";

                //construct the URI for image description
                string visionURI = $"{this.visionEndpoint}/openai/deployments/{this.visionDeploymentModel}/chat/completions?api-version={this.visionAPIVersion.Trim()}";
                var request = new HttpRequestMessage(HttpMethod.Post, visionURI);
                request.Content = new StringContent(messageContent, Encoding.UTF8, "application/json");
                request.Headers.Add("api-key", $"{this.visionApiKey}");
                var response = await client.SendAsync(request);
                if (response.IsSuccessStatusCode)
                {
                    var data = await response.Content.ReadAsStringAsync();
                    var jsonDocument = JsonDocument.Parse(data);
                    var properties = jsonDocument.RootElement.GetProperty("choices");
                    var retMSG = properties[0].GetProperty("message").GetProperty("content").GetString();
                    return retMSG;

                }
                else
                {
                    Console.WriteLine($"Request failed with status code api call {response.StatusCode}");
                }
                return null;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred in describing image: {ex.Message}");
                throw ex;
            }


        }

    }
}
