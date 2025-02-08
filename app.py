import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("GPT Clone")

api_key = os.getenv("LLM_API_KEY")
if not api_key:
    st.error("API key not found.")
    st.stop()

client = Groq(api_key=api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama3-8b-8192"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask your question here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response_text = ""
            placeholder = st.empty()

            # Stream chat completions with direct attribute access
            for chunk in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                # Access attributes directly in the ChatCompletionChunk object
                choice = chunk.choices[0]
                delta_content = choice.delta.content if choice.delta else ""
                if delta_content:
                    response_text += delta_content
                    placeholder.markdown(response_text)

            # Append the final response
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            placeholder.markdown(response_text)

        except Exception as e:
            st.error(f"Error: {e}")
