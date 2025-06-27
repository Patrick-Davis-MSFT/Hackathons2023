using Newtonsoft.Json;
using System;
using System.Collections.Generic;

namespace vi_functions.models
{
    public class VideoIndexResponse
    {
        [JsonProperty("partition")]
        public string Partition { get; set; }

        [JsonProperty("description")]
        public string Description { get; set; }

        [JsonProperty("privacyMode")]
        public string PrivacyMode { get; set; }

        [JsonProperty("state")]
        public string State { get; set; }

        [JsonProperty("accountId")]
        public string AccountId { get; set; }

        [JsonProperty("id")]
        public string Id { get; set; }

        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("userName")]
        public string UserName { get; set; }

        [JsonProperty("created")]
        public string Created { get; set; }

        [JsonProperty("isOwned")]
        public bool IsOwned { get; set; }

        [JsonProperty("isEditable")]
        public bool IsEditable { get; set; }

        [JsonProperty("isBase")]
        public bool IsBase { get; set; }

        [JsonProperty("durationInSeconds")]
        public int DurationInSeconds { get; set; }

        [JsonProperty("duration")]
        public string Duration { get; set; }

        [JsonProperty("summarizedInsights")]
        public SummarizedInsights SummarizedInsights { get; set; }

        [JsonProperty("videos")]
        public List<VideoDetail> Videos { get; set; }

        [JsonProperty("videosRanges")]
        public List<VideoRange> VideosRanges { get; set; }
    }

    public class SummarizedInsights
    {
        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("id")]
        public string Id { get; set; }

        [JsonProperty("privacyMode")]
        public string PrivacyMode { get; set; }

        [JsonProperty("duration")]
        public DurationInfo Duration { get; set; }

        [JsonProperty("thumbnailVideoId")]
        public string ThumbnailVideoId { get; set; }

        [JsonProperty("thumbnailId")]
        public string ThumbnailId { get; set; }

        [JsonProperty("faces")]
        public List<object> Faces { get; set; }

        [JsonProperty("keywords")]
        public List<object> Keywords { get; set; }

        [JsonProperty("sentiments")]
        public List<Sentiment> Sentiments { get; set; }

        [JsonProperty("emotions")]
        public List<object> Emotions { get; set; }

        [JsonProperty("audioEffects")]
        public List<object> AudioEffects { get; set; }

        [JsonProperty("labels")]
        public List<Label> Labels { get; set; }

        [JsonProperty("brands")]
        public List<Brand> Brands { get; set; }

        [JsonProperty("statistics")]
        public Statistics Statistics { get; set; }

        [JsonProperty("topics")]
        public List<object> Topics { get; set; }
    }

    public class DurationInfo
    {
        [JsonProperty("time")]
        public string Time { get; set; }

        [JsonProperty("seconds")]
        public double Seconds { get; set; }
    }

    public class Sentiment
    {
        [JsonProperty("sentimentKey")]
        public string SentimentKey { get; set; }

        [JsonProperty("seenDurationRatio")]
        public double SeenDurationRatio { get; set; }

        [JsonProperty("appearances")]
        public List<TimeRange> Appearances { get; set; }
    }

    public class TimeRange
    {
        [JsonProperty("startTime")]
        public string StartTime { get; set; }

        [JsonProperty("endTime")]
        public string EndTime { get; set; }

        [JsonProperty("startSeconds")]
        public double StartSeconds { get; set; }

        [JsonProperty("endSeconds")]
        public double EndSeconds { get; set; }
    }

    public class Label
    {
        [JsonProperty("id")]
        public int Id { get; set; }

        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("appearances")]
        public List<LabelAppearance> Appearances { get; set; }
    }

    public class LabelAppearance
    {
        [JsonProperty("confidence")]
        public double Confidence { get; set; }

        [JsonProperty("startTime")]
        public string StartTime { get; set; }

        [JsonProperty("endTime")]
        public string EndTime { get; set; }

        [JsonProperty("startSeconds")]
        public double StartSeconds { get; set; }

        [JsonProperty("endSeconds")]
        public double EndSeconds { get; set; }
    }

    public class Brand
    {
        [JsonProperty("id")]
        public int Id { get; set; }

        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("referenceId")]
        public string ReferenceId { get; set; }

        [JsonProperty("referenceUrl")]
        public string ReferenceUrl { get; set; }

        [JsonProperty("confidence")]
        public double Confidence { get; set; }

        [JsonProperty("description")]
        public string Description { get; set; }

        [JsonProperty("seenDuration")]
        public double SeenDuration { get; set; }

        [JsonProperty("appearances")]
        public List<TimeRange> Appearances { get; set; }
    }

    public class VideoDetail
    {
        [JsonProperty("accountId")]
        public string AccountId { get; set; }

        [JsonProperty("id")]
        public string Id { get; set; }

        [JsonProperty("state")]
        public string State { get; set; }

        [JsonProperty("moderationState")]
        public string ModerationState { get; set; }

        [JsonProperty("reviewState")]
        public string ReviewState { get; set; }

        [JsonProperty("privacyMode")]
        public string PrivacyMode { get; set; }

        [JsonProperty("processingProgress")]
        public string ProcessingProgress { get; set; }

        [JsonProperty("failureMessage")]
        public string FailureMessage { get; set; }

        [JsonProperty("externalId")]
        public string ExternalId { get; set; }

        [JsonProperty("externalUrl")]
        public string ExternalUrl { get; set; }

        [JsonProperty("metadata")]
        public object Metadata { get; set; }

        [JsonProperty("insights")]
        public VideoInsights Insights { get; set; }

        [JsonProperty("width")]
        public int Width { get; set; }

        [JsonProperty("height")]
        public int Height { get; set; }

        [JsonProperty("detectSourceLanguage")]
        public bool DetectSourceLanguage { get; set; }

        [JsonProperty("languageAutoDetectMode")]
        public string LanguageAutoDetectMode { get; set; }

        [JsonProperty("sourceLanguage")]
        public string SourceLanguage { get; set; }

        [JsonProperty("sourceLanguages")]
        public List<string> SourceLanguages { get; set; }

        [JsonProperty("language")]
        public string Language { get; set; }

        [JsonProperty("languages")]
        public List<string> Languages { get; set; }

        [JsonProperty("indexingPreset")]
        public string IndexingPreset { get; set; }

        [JsonProperty("streamingPreset")]
        public string StreamingPreset { get; set; }

        [JsonProperty("isAdult")]
        public bool IsAdult { get; set; }

        [JsonProperty("isSearchable")]
        public bool IsSearchable { get; set; }

        [JsonProperty("publishedUrl")]
        public string PublishedUrl { get; set; }

        [JsonProperty("publishedProxyUrl")]
        public string PublishedProxyUrl { get; set; }

        [JsonProperty("viewToken")]
        public string ViewToken { get; set; }
    }

    public class VideoInsights
    {
        [JsonProperty("version")]
        public string Version { get; set; }

        [JsonProperty("duration")]
        public string Duration { get; set; }

        [JsonProperty("sourceLanguage")]
        public string SourceLanguage { get; set; }

        [JsonProperty("sourceLanguages")]
        public List<string> SourceLanguages { get; set; }

        [JsonProperty("language")]
        public string Language { get; set; }

        [JsonProperty("languages")]
        public List<string> Languages { get; set; }

        [JsonProperty("transcript")]
        public List<TranscriptItem> Transcript { get; set; }

        [JsonProperty("keywords")]
        public List<Keyword> Keywords { get; set; }

        [JsonProperty("labels")]
        public List<InsightLabel> Labels { get; set; }

        [JsonProperty("brands")]
        public List<InsightBrand> Brands { get; set; }

        [JsonProperty("sentiments")]
        public List<InsightSentiment> Sentiments { get; set; }

        [JsonProperty("textualContentModeration")]
        public TextualContentModeration TextualContentModeration { get; set; }

        [JsonProperty("statistics")]
        public Statistics Statistics { get; set; }
    }

    public class Keyword
    {
        [JsonProperty("id")]
        public int Id { get; set; }

        [JsonProperty("text")]
        public string Text { get; set; }

        [JsonProperty("confidence")]
        public double Confidence { get; set; }

        [JsonProperty("language")]
        public string Language { get; set; }

        [JsonProperty("instances")]
        public List<KeywordInstance> Instances { get; set; }
    }

    public class KeywordInstance
    {
        [JsonProperty("adjustedStart")]
        public string AdjustedStart { get; set; }

        [JsonProperty("adjustedEnd")]
        public string AdjustedEnd { get; set; }

        [JsonProperty("start")]
        public string Start { get; set; }

        [JsonProperty("end")]
        public string End { get; set; }
    }

    public class InsightLabel
    {
        [JsonProperty("id")]
        public int Id { get; set; }

        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("referenceId")]
        public string ReferenceId { get; set; }

        [JsonProperty("language")]
        public string Language { get; set; }

        [JsonProperty("instances")]
        public List<LabelInstance> Instances { get; set; }
    }

    public class LabelInstance
    {
        [JsonProperty("confidence")]
        public double Confidence { get; set; }

        [JsonProperty("adjustedStart")]
        public string AdjustedStart { get; set; }

        [JsonProperty("adjustedEnd")]
        public string AdjustedEnd { get; set; }

        [JsonProperty("start")]
        public string Start { get; set; }

        [JsonProperty("end")]
        public string End { get; set; }
    }

    public class InsightBrand
    {
        [JsonProperty("id")]
        public int Id { get; set; }

        [JsonProperty("referenceType")]
        public string ReferenceType { get; set; }

        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("referenceId")]
        public string ReferenceId { get; set; }

        [JsonProperty("referenceUrl")]
        public string ReferenceUrl { get; set; }

        [JsonProperty("description")]
        public string Description { get; set; }

        [JsonProperty("tags")]
        public List<object> Tags { get; set; }

        [JsonProperty("confidence")]
        public double Confidence { get; set; }

        [JsonProperty("isCustom")]
        public bool IsCustom { get; set; }

        [JsonProperty("instances")]
        public List<BrandInstance> Instances { get; set; }
    }

    public class BrandInstance
    {
        [JsonProperty("brandType")]
        public string BrandType { get; set; }

        [JsonProperty("instanceSource")]
        public string InstanceSource { get; set; }

        [JsonProperty("adjustedStart")]
        public string AdjustedStart { get; set; }

        [JsonProperty("adjustedEnd")]
        public string AdjustedEnd { get; set; }

        [JsonProperty("start")]
        public string Start { get; set; }

        [JsonProperty("end")]
        public string End { get; set; }
    }

    public class InsightSentiment
    {
        [JsonProperty("id")]
        public int Id { get; set; }

        [JsonProperty("averageScore")]
        public double AverageScore { get; set; }

        [JsonProperty("sentimentType")]
        public string SentimentType { get; set; }

        [JsonProperty("instances")]
        public List<SentimentInstance> Instances { get; set; }
    }

    public class SentimentInstance
    {
        [JsonProperty("adjustedStart")]
        public string AdjustedStart { get; set; }

        [JsonProperty("adjustedEnd")]
        public string AdjustedEnd { get; set; }

        [JsonProperty("start")]
        public string Start { get; set; }

        [JsonProperty("end")]
        public string End { get; set; }
    }

    public class TranscriptItem
    {
        [JsonProperty("id")]
        public int Id { get; set; }

        [JsonProperty("text")]
        public string Text { get; set; }

        [JsonProperty("confidence")]
        public double Confidence { get; set; }

        [JsonProperty("speakerId")]
        public int SpeakerId { get; set; }

        [JsonProperty("language")]
        public string Language { get; set; }

        [JsonProperty("instances")]
        public List<TranscriptInstance> Instances { get; set; }
    }

    public class TranscriptInstance
    {
        [JsonProperty("adjustedStart")]
        public string AdjustedStart { get; set; }

        [JsonProperty("adjustedEnd")]
        public string AdjustedEnd { get; set; }

        [JsonProperty("start")]
        public string Start { get; set; }

        [JsonProperty("end")]
        public string End { get; set; }
    }

    public class TextualContentModeration
    {
        [JsonProperty("id")]
        public int Id { get; set; }

        [JsonProperty("bannedWordsCount")]
        public int BannedWordsCount { get; set; }

        [JsonProperty("bannedWordsRatio")]
        public double BannedWordsRatio { get; set; }

        [JsonProperty("instances")]
        public List<object> Instances { get; set; }
    }

    public class Statistics
    {
        [JsonProperty("correspondenceCount")]
        public int CorrespondenceCount { get; set; }

        [JsonProperty("speakerTalkToListenRatio")]
        public Dictionary<string, double> SpeakerTalkToListenRatio { get; set; }

        [JsonProperty("speakerLongestMonolog")]
        public Dictionary<string, int> SpeakerLongestMonolog { get; set; }

        [JsonProperty("speakerNumberOfFragments")]
        public Dictionary<string, int> SpeakerNumberOfFragments { get; set; }

        [JsonProperty("speakerWordCount")]
        public Dictionary<string, int> SpeakerWordCount { get; set; }
    }

    public class VideoRange
    {
        [JsonProperty("videoId")]
        public string VideoId { get; set; }

        [JsonProperty("range")]
        public Range Range { get; set; }
    }

    public class Range
    {
        [JsonProperty("start")]
        public string Start { get; set; }

        [JsonProperty("end")]
        public string End { get; set; }
    }
}