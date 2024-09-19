using Microsoft.SemanticKernel;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;
using System.Text.Json.Serialization;
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;
using Microsoft.Azure.Search.Common;

namespace chat_app.plugins
{
    internal class AzureAISearchPlugin
    {

        private string searchIndexName { get; set; }
        private string searchQueryApiKey { get; set; }
        private string searchEndpoint { get; set; }
        private static SearchClient searchClient;
        internal AzureAISearchPlugin(string searchIndexName, string searchQueryApiKey, string searchEndpoint)
        {
            this.searchIndexName = searchIndexName;
            this.searchQueryApiKey = searchQueryApiKey;
            this.searchEndpoint = searchEndpoint;
            searchClient = new SearchClient(
                new Uri(searchEndpoint),
                searchIndexName,
                new AzureKeyCredential(searchQueryApiKey)
            );
        }

        private static readonly HttpClient client = new HttpClient();

        [KernelFunction("seach_campingInfo")]
        [Description("Searches an index of information on camping")]
        [return: Description("Returns information on camping based on a search term")]
        public static async Task<searchResults[]> GetSearchQuery(string searchTerm)
        {
            try
            {
                var options = new SearchOptions
                {
                    QueryType = SearchQueryType.Semantic,
                    IncludeTotalCount = true,
                    SearchMode = SearchMode.All,
                    Size = 10,
                };


                var response = await searchClient.SearchAsync<SearchDocument>(searchTerm, options);
                var result = response.Value.GetResults();
                var searchResults = new List<searchResults>();
                foreach (var res in result)
                {
                    searchResults tmp = new searchResults
                    {
                        chunk = res.Document.GetString("chunk"),
                        title = res.Document.GetString("title")
                    };
                    searchResults.Add(tmp);
                }

                return searchResults.ToArray();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"A Search error occurred: {ex.Message}");
                return null;
            }
        }

        internal class searchResults
        {

            [JsonPropertyName("chunk")]
            public string chunk { get; set; }
            [JsonPropertyName("title")]
            public string title { get; set; }
        }

    }
}
