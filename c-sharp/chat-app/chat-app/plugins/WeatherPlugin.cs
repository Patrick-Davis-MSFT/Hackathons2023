using Microsoft.SemanticKernel;
using System;
using System.ComponentModel;
using System.Net.Http;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace chat_app.plugins
{
    internal class WeatherPlugin
    {
        private static readonly HttpClient client = new HttpClient();

        [KernelFunction("get_weather")]
        [Description("Gets a json response of the weather")]
        [return: Description("Returns a textual forecast for a 2.5km grid area")]
        public static async Task<weatherPeriod[]> GetLatLongWeatherAsync(double latitude, double longitude)
        {
            try
            {
                // First API call to get grid information
                var request = new HttpRequestMessage(HttpMethod.Get, $"https://api.weather.gov/points/{latitude},{longitude}");
                request.Headers.Add("Accept", "*/*");
                request.Headers.Add("User-Agent", "sample.sample");
                var response = await client.SendAsync(request);
                if (response.IsSuccessStatusCode)
                {
                    var data = await response.Content.ReadAsStringAsync();
                    var jsonDocument = JsonDocument.Parse(data);
                    var properties = jsonDocument.RootElement.GetProperty("properties");
                    string office = properties.GetProperty("gridId").GetString();
                    int gridX = properties.GetProperty("gridX").GetInt32();
                    int gridY = properties.GetProperty("gridY").GetInt32();



                    // Second API call to get weather forecast
                    request = new HttpRequestMessage(HttpMethod.Get, $"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast");
                    request.Headers.Add("Accept", "*/*");
                    request.Headers.Add("User-Agent", "sample.sample");
                    response = await client.SendAsync(request);
                    if (response.IsSuccessStatusCode)
                    {
                        data = await response.Content.ReadAsStringAsync();
                        jsonDocument = JsonDocument.Parse(data);
                        var periods = jsonDocument.RootElement.GetProperty("properties").GetProperty("periods");

                        var weatherPeriods = JsonSerializer.Deserialize<weatherPeriod[]>(periods.GetRawText());
                        return weatherPeriods;
                    }
                    else
                    {
                        Console.WriteLine($"Request failed with status code step 2 {response.StatusCode}");
                    }
                }
                else
                {
                    Console.WriteLine($"Request failed with status code step 1 {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }

            return Array.Empty<weatherPeriod>();
        }
    }

    public class probPrecip
    {
        [JsonPropertyName("unitCode")]
        public string? unitCode { get; set; }
        [JsonPropertyName("value")]
        public int? value { get; set; }
    }

    public class weatherPeriod
    {
        [JsonPropertyName("number")]
        public int number { get; set; }
        [JsonPropertyName("name")]
        public string name { get; set; }
        [JsonPropertyName("startTime")]
        public DateTime startTime { get; set; }
        [JsonPropertyName("endTime")]
        public DateTime endTime { get; set; }
        [JsonPropertyName("isDayTime")]
        public bool isDayTime { get; set; }
        [JsonPropertyName("temperature")]
        public int temperature { get; set; }
        [JsonPropertyName("temperatureUnit")]
        public string temperatureUnit { get; set; }
        [JsonPropertyName("temperatureTrend")]
        public string unit { get; set; }
        [JsonPropertyName("probabilityOfPrecipitation")]
        public probPrecip? probabilityOfPrecipitation { get; set; }
        [JsonPropertyName("windSpeed")]
        public string windSpeed { get; set; }
        [JsonPropertyName("windDirection")]
        public string windDirection { get; set; }
        [JsonPropertyName("icon")]
        public string icon { get; set; }
        [JsonPropertyName("shortForecast")]
        public string shortForecast { get; set; }
        [JsonPropertyName("detailedForecast")]
        public string detailedForecast { get; set; }

    }
}
