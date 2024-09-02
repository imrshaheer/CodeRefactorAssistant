import streamlit as st
import os
from utils import systemPrompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Constants for clarity and potential future changes
GOOGLE_API_KEY_ENV_VAR = "GOOGLE_API_KEY"
MODEL_NAME = "gemini-1.5-flash"

def init():
    # Streamlit page setup
    st.set_page_config(
        page_title="CodeRefactorAssistant!",
        page_icon="🤖"
    )

def load_llm(model_name):
    """Loads the LLM based on the provided model name."""
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

def display_messages(messages):
    """Displays the chat messages in the Streamlit app."""
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            with st.chat_message("Human"):
                st.write(msg.content)
        else:
            with st.chat_message("AI"):
                st.write(msg.content)

def main():
    """Main function to run the Streamlit app."""
    init()

    st.header("Your Code Refactor Assistant! 🤖")
    st.write("Guiding You to Better Code with Best Practices")

    # Sidebar for API key input
    with st.sidebar:
        st.header("API Key")
        api_key = st.text_input("Enter your Google API Key:", type="password")
        if api_key:
            os.environ[GOOGLE_API_KEY_ENV_VAR] = api_key
            st.success("API Key saved!")
        else:
            st.info(f"{GOOGLE_API_KEY_ENV_VAR} is not set.")
            st.stop()

    # Initialize LLM using the load_llm function
    llm = load_llm(MODEL_NAME)

    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=systemPrompt())
        ]

    user_input = st.chat_input("Your message: ", key="user_input")

    # Handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(
            AIMessage(content=response.content))

    # Display messages using the display_messages function
    display_messages(st.session_state.messages)

if __name__ == "__main__":
    main()