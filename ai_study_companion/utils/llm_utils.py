import google.generativeai as genai
import os

# Setup Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def call_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Error calling Gemini: {e}]"

def summarize_mission(content):
    prompt = f"""Summarize the following content from a Pega mission step. 
Provide a TL;DR and bullet points.

Content:
{content}
"""
    return call_gemini(prompt)

def extract_key_concepts(content):
    prompt = f"""Read the following Pega training content and extract the 5-10 most important concepts to remember.

Content:
{content}
"""
    return call_gemini(prompt)

def generate_quiz(content):
    prompt = f"""Based on this Pega training content, generate a quiz with:
- 3 multiple-choice questions
- 2 true/false
- 1 fill-in-the-blank

Include the answers.

Content:
{content}
"""
    return call_gemini(prompt)

def create_study_plan(content, days=7):
    prompt = f"""
    You are an expert study planner. Given the following mission content, create a daily study plan spread over {days} days.

    Output the plan in strict JSON format like this:
    [
      {{
        "day": 1,
        "title": "Introduction to Pega",
        "goal": "Understand what Pega is and explore Dev Studio.",
        "topics": ["What is Pega?", "Dev Studio overview"]
      }},
      ...
    ]
    Content:
    {content}
    """
    return call_gemini(prompt)



def answer_question_with_rag(question, vectorstore, top_k=3, relevance_threshold=0.7):
    # Get docs *with* similarity scores
    results = vectorstore.similarity_search_with_score(question, k=top_k)

    if not results or all(score < relevance_threshold for _, score in results):
        # No good matches: fallback to Gemini general knowledge
        fallback_prompt = f"""
        You're a helpful AI assistant. Answer the following question using your general knowledge:

        Question: {question}
        """
        return call_gemini(fallback_prompt).strip() + "\n\n🌐 Answered from Gemini's general knowledge."

    # Prepare context from top-k results
    context = "\n\n".join(doc.page_content for doc, score in results)
    prompt = f"""
    You're a helpful assistant. Use the following mission content to answer the question.

    Content:
    {context}

    Question: {question}

    Provide a helpful answer.
    """
    return call_gemini(prompt).strip() + "\n\n📚 Based on mission content."

def evaluate_summary(summary: str) -> str:
    prompt = f"""
You are an expert reviewer. Evaluate the following summary of a learning module.

Your evaluation should include:
- Overall Clarity (Is it easy to understand?)
- Accuracy (Does it seem factually and contextually correct?)
- Completeness (Does it miss anything important?)
- Suggestions for Improvement (if any)

### Summary:
{summary}

Please provide a constructive evaluation in markdown format.
"""
    return call_gemini(prompt)


def evaluate_quiz(quiz: str) -> str:
    prompt = f"""
You are an expert evaluator. Review the quality of the following quiz.

Evaluate on:
- Relevance to the topic
- Clarity of questions
- Variety and difficulty level
- Answer accuracy (if answers are included)

### Quiz:
{quiz}

Provide your review in markdown format and suggest improvements if needed.
"""
    return call_gemini(prompt)





