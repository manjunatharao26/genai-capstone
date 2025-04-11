import json
import streamlit as st
from .llm_utils import call_gemini  # Updated to use relative import


# Commented out the function for now
# def create_study_plan_json(mission_text: str, days: int):
#     """
#     Use Gemini to generate a JSON-structured study plan for the mission.
#     """
#     prompt = f"""
# You are an AI study planner. Generate a structured study plan for the following content:
#
# Content:
# {mission_text}
#
# The user wants to complete it in {days} days.
#
# Return the plan strictly in JSON format like:
# [
#   {{
#     "day": 1,
#     "title": "Topic title",
#     "objectives": ["objective1", "objective2"],
#     "notes": "Extra details"
#   }},
#   ...
# ]
#     """
#     response = call_gemini(prompt)
#
#     try:
#         # Ensure the response is not empty
#         if not response:
#             return "❌ Error: Received an empty response from the AI model."
#
#         # Check if the response is already a valid JSON object
#         if isinstance(response, str):
#             plan = json.loads(response)
#         else:
#             plan = response
#             print(plan)
#
#         # Validate the structure of the JSON
#         if not isinstance(plan, list):
#             return "❌ Error: The response is not a valid JSON list."
#
#         return plan
#     except json.JSONDecodeError as e:
#         return f"❌ Error parsing JSON: {e}\n\nRaw response:\n{response}"
#     except Exception as e:
#         return f"❌ Unexpected error: {e}\n\nRaw response:\n{response}"


def create_study_plan_json(mission_text: str, days: int):
    """
    Use Gemini to generate a JSON-structured study plan for the mission.
    """
    prompt = f"""
You are an AI study planner. Generate a structured study plan for the following content:

Content:
{mission_text}

The user wants to complete it in {days} days.

Return the plan strictly in JSON format like:
[
  {{
    "day": 1,
    "title": "Topic title",
    "objectives": ["objective1", "objective2"],
    "notes": "Extra details"
  }},
  ...
]
    """
    response = call_gemini(prompt)

    try:
        # Ensure the response is not empty
        if not response or not response.strip():
            return "❌ Error: Received an empty or invalid response from the AI model."

        # Attempt to parse the response as JSON
        #remove ```json from start of response
        if response.startswith("```json"):
            response = response[7:].strip()
        #remove ``` from end of response
        if response.endswith("```"):
            response = response[:-3].strip()
        plan = json.loads(response)

        # Validate the structure of the JSON
        if not isinstance(plan, list):
            return "❌ Error: The response is not a valid JSON list."

        return plan
    except json.JSONDecodeError as e:
        return f"❌ Error parsing JSON: {e}\n\nRaw response:\n{response}"
    except Exception as e:
        return f"❌ Unexpected error: {e}\n\nRaw response:\n{response}"


def render_timeline(plan_json: list):
    """
    Display the structured study plan in a Streamlit timeline-like UI.
    """
    for day in plan_json:
        with st.expander(f"📅 Day {day.get('day', '?')}: {day.get('title', '')}", expanded=True):
            st.markdown("**Objectives:**")
            for obj in day.get("objectives", []):
                st.markdown(f"- {obj}")
            if notes := day.get("notes"):
                st.markdown(f"**Notes:** {notes}")


