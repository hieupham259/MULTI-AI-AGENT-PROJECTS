import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

# Compose backend API endpoint from settings so it can be overridden via env var
API_URL = "http://127.0.0.1:9999/api/chat"


def render() -> None:
    """Render the Streamlit UI and handle interactions."""
    # Must be the first Streamlit command
    st.set_page_config(page_title="Multi AI Agents", layout="centered")
    st.title("Multi AI Agents using multi Gemini models and Tavily Search")

    # Use a form to avoid side effects on every widget interaction/rerun
    with st.form("agent_form"):
        system_prompt = st.text_area("Define your AI Agent:", height=70, key="system_prompt")
        selected_model = st.selectbox("Select your AI model:", settings.ALLOWED_MODEL_NAMES, key="selected_model")
        allow_web_search = st.checkbox("Allow web search", key="allow_search")
        user_query = st.text_area("Enter your query:", height=150, key="user_query")
        # On the submit run, this returns True; we also set a fallback click flag
        submitted = st.form_submit_button(
            "Ask Agent",
            on_click=lambda: st.session_state.update({"submit_clicked": True})
        )

    logger.info("Submit button clicked? %s", submitted)
    # Fallback: if for any reason the return value is False on this run,
    # check a one-shot session flag set by on_click. Pop it so it's consumed once.
    if not submitted:
        submitted = st.session_state.pop("submit_clicked", False)

    if submitted:
        # Validate input first
        logger.info("Form submitted: validating input")

        if not user_query or not user_query.strip():
            st.warning("Please enter a query before asking the agent.")
            logger.warning("User submitted empty query.")
        else:
            payload = {
                "model_name": selected_model,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search,
            }

            try:
                logger.info("Sending request to backend API")

                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    agent_response = response.json().get("response", "")
                    logger.info("Successfully received response from backend")

                    # Persist response to show outside the form (avoids double-render on rerun)
                    st.session_state["last_response"] = agent_response
                else:
                    logger.error("Backend returned non-200 status: %s", response.status_code)
                    st.error("Error with backend")
            except Exception as e:
                logger.exception("Error occurred while sending request to backend")
                st.error(str(CustomException("Failed to communicate to backend")))
    else:
        logger.info("Form not submitted yet")

    # Show last response (if any) outside the form so it persists across reruns
    if "last_response" in st.session_state and st.session_state["last_response"]:
        st.subheader("Agent Response")
        st.markdown(st.session_state["last_response"].replace("\n", "<br>"), unsafe_allow_html=True)
    else:
        st.info("Enter your query and click 'Ask Agent' to run.")


if __name__ == "__main__":
    render()
