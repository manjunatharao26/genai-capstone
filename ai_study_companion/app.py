from utils.scrape_mission import get_pega_mission_steps
from utils.llm_utils import summarize_mission, extract_key_concepts, generate_quiz, create_study_plan, answer_question_with_rag,evaluate_quiz,evaluate_summary
from utils.timeline_utils import create_study_plan_json, render_timeline
from utils.vectore_store import create_vector_store
import streamlit as st
import datetime
import sys
import os

# Add the project directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

import google.generativeai
from genai_urlsumriz.utils.youtube_utils import summarize_url
from genai_urlsumriz.utils.news_utils import get_news_article_text

st.set_page_config(page_title="AI Study Companion & URL Summarizer", layout="wide")
st.title("🧠 AI Study Companion & URL Summarizer")

# --- Sidebar Inputs ---
with st.sidebar:
    # st.image("assets/logo.png", width=200)
    st.write("## Welcome to AI Study Companion & URL Summarizer")
    app_mode = st.radio("Choose Application Mode:", ("Pega Study Companion", "URL Summarizer"))

if app_mode == "Pega Study Companion":
    st.header("Pega Study Companion")
    mission_url = st.text_input("Enter Pega Academy Mission URL:",
                                placeholder="https://academy.pega.com/mission/system-architect/v7")
    study_days = st.slider("How many days do you want to study this mission?", 3, 21, 7)
    if st.button("🧪 Generate Study Guide"):
        if mission_url:
            with st.spinner("Scraping mission and generating AI outputs..."):
                steps = get_pega_mission_steps(mission_url)
                combined_text = "\n\n".join([step['text'] for step in steps[:5]])  # you can change range

                st.session_state['combined_text'] = combined_text
                st.session_state['vectorstore'] = create_vector_store(combined_text)
                st.session_state['summary'] = summarize_mission(combined_text)
                st.session_state['concepts'] = extract_key_concepts(combined_text)
                st.session_state['quiz'] = generate_quiz(combined_text)
                st.session_state['plan']  = create_study_plan_json(combined_text, study_days)
                #st.session_state['plan'] = create_study_plan(combined_text, study_days)

    # --- Main Content Tabs ---
    if "combined_text" in st.session_state:
        tabs = st.tabs(["📘 Summary", "🧠 Key Concepts", "❓ Quiz", "🗓️ Study Plan", "🔍 Ask me anything", "📊 Evaluate AI Output"])

        with tabs[0]:
            st.markdown(st.session_state['summary'])

        with tabs[1]:
            st.markdown(st.session_state['concepts'])

        with tabs[2]:
            st.markdown(st.session_state['quiz'])

        with tabs[3]:
                plan_json=st.session_state['plan']
                if isinstance(plan_json, list):
                    render_timeline(plan_json)
                else:
                    st.error("❌ Failed to generate a structured study plan.")
                    st.code(plan_json)  # shows error or raw response

        with tabs[4]:
            st.subheader("🧠 Ask me anything from this mission")

            # Initialize chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # Clear history button
            if st.button("🧹 Clear Chat History"):
                st.session_state.chat_history = []
                st.success("Chat history cleared!")

            user_question = st.text_input("Type your question here and press Enter", key="rag_question")

            if user_question:
                with st.spinner("Thinking..."):
                    rag_answer = answer_question_with_rag(user_question, st.session_state.vectorstore)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": rag_answer,
                    "time": timestamp
                })

            # Show chat history (always expanded)
            st.markdown("### 💬 Chat History")
            for i, qa in enumerate(reversed(st.session_state.chat_history), 1):
                st.markdown(f"**🕒 {qa['time']}**")
                st.markdown(f"**❓ Question {i}:** {qa['question']}")
                st.markdown(f"**🤖 Answer:** {qa['answer']}")
                st.markdown("---")

        with tabs[5]:
            st.subheader("📊 Evaluate Summary and Quiz Quality")

            if st.button("🔍 Evaluate Summary"):
                with st.spinner("Evaluating summary..."):
                    summary_eval = evaluate_summary(st.session_state['summary'] )
                st.markdown("### ✅ Summary Evaluation")
                st.markdown(summary_eval)

            if st.button("📝 Evaluate Quiz"):
                with st.spinner("Evaluating quiz..."):
                    quiz_eval = evaluate_quiz(st.session_state['quiz'] )
                st.markdown("### ✅ Quiz Evaluation")
                st.markdown(quiz_eval)

    else:
        st.info("🔍 Enter a Pega mission URL and click 'Generate Study Guide' from the sidebar to get started.")

elif app_mode == "URL Summarizer":
    st.header("URL Summarizer")
    st.write("Enter the URL of a YouTube video or any web article to get a summary.")

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
