import re
from youtube_transcript_api import YouTubeTranscriptApi
from genai_urlsumriz.utils.summarizer import summarize_content

def is_youtube_url(url: str) -> bool:
    return 'youtube.com/watch' in url or 'youtu.be/' in url

def extract_video_id(url: str) -> str:
    if 'youtu.be/' in url:
        return url.split('/')[-1]
    match = re.search(r"v=([\w-]+)", url)
    return match.group(1) if match else None

def get_youtube_transcript(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        return "[Transcript unavailable due to IP restrictions. Please provide transcript manually.]"

def summarize_url(url: str):
    if is_youtube_url(url):
        video_id = extract_video_id(url)
        if not video_id:
            print("Invalid YouTube URL.")
            return
        print("Fetching YouTube transcript...")
        content = get_youtube_transcript(video_id)
    else:
        print("Fetching news article text...")
        from genai_urlsumriz.utils.news_utils import get_news_article_text
        content = get_news_article_text(url)

    print("Generating summary with LLM...")
    summary = summarize_content(content)
    print(f"Summary:\n{summary}")

def summarize_url(url: str) ->str:
    if is_youtube_url(url):
        video_id = extract_video_id(url)
        if not video_id:
            print("Invalid YouTube URL.")
            return
        print("Fetching YouTube transcript...")
        content = get_youtube_transcript(video_id)
    else:
        print("Fetching news article text...")
        from genai_urlsumriz.utils.news_utils import get_news_article_text
        content = get_news_article_text(url)

    print("Generating summary with LLM...")
    summary = summarize_content(content)
    print(f"Summary:\n{summary}")
    return summary