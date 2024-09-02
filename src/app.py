# python 3.8 (3.8.16) or it doesn't work
# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from dotenv import load_dotenv
import os
from utils import systemPrompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()
    
    # test that the API key exists
    if os.getenv("GOOGLE_API_KEY") is None or os.getenv("GOOOGLE_API_KEY") == "":
        print("GOOGLE_API_KEY is not set")
        exit(1)
    else:
        print("GOOGLE_API_KEY is set")

    # setup streamlit page
    st.set_page_config(
        page_title="RefactorAssistant!",
        page_icon="🤖"
    )


def main():
    init()

    st.header("Your Code Refactor Assistant! 🤖")
    st.write("Guiding You to Better Code with Best Practices")

    llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                # other params...
            )
    
    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=systemPrompt())
        ]

    user_input = st.chat_input("Your message: ", key="user_input")

    # handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(
            AIMessage(content=response.content))
        
    # st.write(st.session_state.messages)

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            with st.chat_message("Human"):
                st.write(msg.content)
        else:
            with st.chat_message("AI"):
                st.write(msg.content)
    



if __name__ == "__main__":
    main()