import google.generativeai as genai

def call_llm(prompt: str) -> str:
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gemini API Error: {e}]"

def summarize_content(content: str) -> str:
    if not content or "Transcript unavailable" in content:
        return "[No content available to summarize.]"

    prompt = (
        "You're a helpful assistant. Summarize the following content. "
        "Provide a TL;DR followed by 3-5 bullet points for key takeaways.\n\n"
        f"{content}"
    )
    return call_llm(prompt)