import streamlit as st
import sys
import os

# Add the project directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

import google.generativeai
from genai_urlsumriz.utils.youtube_utils import summarize_url
from genai_urlsumriz.utils.news_utils import get_news_article_text

# Streamlit UI
st.title("GenAI Capstone - URL Summarizer")
st.write("Enter the URL of a YouTube video or a news article to get a summary.")

# Add LinkedIn profile badge
st.markdown("""
<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
            
<div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="manjunatharao26" data-version="v1">
    <a class="badge-base__link LI-simple-link" href="https://in.linkedin.com/in/manjunatharao26?trk=profile-badge">Manjunatha Rao</a>
</div>
""", 
unsafe_allow_html=True)

url = st.text_input("Enter URL:", placeholder="https://www.youtube.com/watch?v=example or https://news.example.com/article")
st.session_state.url = url  # Store the URL in session state

if st.button("Summarize"):
    if st.session_state.url:  # Ensure the session state is used
        try:
            summary = summarize_url(st.session_state.url)
            st.subheader("Summary:")
            st.write(summary)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")
