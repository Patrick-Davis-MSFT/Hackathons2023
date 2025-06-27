using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace vi_functions.models
{
    namespace vi_functions.models
    {
        public class VideoIndexerTokenResponse
        {
            [JsonProperty("accessToken")]
            public string AccessToken { get; set; }
        }
    }
}
