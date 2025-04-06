import sys
import os
import google.generativeai as genai

# Check for GOOGLE_API_KEY environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
else:
    raise EnvironmentError("GOOGLE_API_KEY environment variable not set. Please set it or configure the API key programmatically.")

# Add the project directory to the Python path
directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(directory)
sys.path.append(parent_directory)

from genai_urlsumriz.utils.youtube_utils import summarize_url
from genai_urlsumriz.utils.news_utils import get_news_article_text

if __name__ == "__main__":
    url = input("Enter the full path to your YT video/news article: ")
    summarize_url(url)