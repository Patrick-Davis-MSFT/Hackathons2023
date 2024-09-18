using System;
using System.IO;
using Newtonsoft.Json;

namespace chat_app.config
{
    public class SettingsProps
    {
        // Define properties that match the structure of your settings.json file
        public string deploymentId { get; set; }
        public string endpoint { get; set; }
        public string apiKey { get; set; }
        public string searchIndexName { get; set; }
        public string searchQueryApiKey { get; set; }
        public string searchEndpoint { get; set; }
        public string visionDeploymentModel { get; set; }
        public string visionEndpoint { get; set; }
        public string visionApiKey { get; set; }
        public string visionAPIVersion { get; set; }
    }

    internal class Settings
    {
        public SettingsProps config { get; set; }
        public Settings()
        {
            string filePath = "./config/settings.json";
            try
            {
                // Read the file content
                string jsonContent = File.ReadAllText(filePath);

                // Deserialize the JSON content into the Settings object
                config = JsonConvert.DeserializeObject<SettingsProps>(jsonContent);

            }
            catch (FileNotFoundException)
            {
                Console.WriteLine("The settings.json file was not found.");
            }
            catch (JsonException)
            {
                Console.WriteLine("Error parsing the settings.json file.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An unexpected error occurred: {ex.Message}");
            }
        }
    }
}
