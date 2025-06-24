using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace vi_functions.models
{
    internal class VideoIndexerResult
    {
        [JsonProperty("accountId")]
        public string? AccountId { get; set; }

        [JsonProperty("id")]
        public string? Id { get; set; }

        [JsonProperty("name")]
        public string? Name { get; set; }

        [JsonProperty("description")]
        public string? Description { get; set; }

        [JsonProperty("created")]
        public string? Created { get; set; }

        [JsonProperty("privacyMode")]
        public string? PrivacyMode { get; set; }

        [JsonProperty("state")]
        public string? State { get; set; }

        // Additional properties for our database
        public string? OriginalFileName { get; set; }
        public DateTime ProcessedDate { get; set; }
    }
}
