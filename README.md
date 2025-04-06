# genai-capstone

Lets experiment with AI
https://genai-summarize.streamlit.app/

## Setting Up the API Key

To use the Gemini API, you need to set the `GOOGLE_API_KEY` environment variable. 

Alternatively, you can configure the API key programmatically in the code.

## Running the Application Locally

To run the application locally using Streamlit, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/genai-capstone.git
    cd genai-capstone
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set the `GOOGLE_API_KEY` environment variable:
    ```sh
    export GOOGLE_API_KEY='your_api_key'  # On Windows use `set GOOGLE_API_KEY=your_api_key`
    ```

5. Run the Streamlit application:
    ```sh
    streamlit run genai_urlsumriz/app.py  # To run the URL summarize app- this can summarize any YouTube URLs or web articles.
    streamlit run ai_study_companion/app.py  # To run the second app- this will launch with radio button for both apps. This app is a companion for pega study missions
    ```

Now you can access the application in your web browser at `http://localhost:8501`.
