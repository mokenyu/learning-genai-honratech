import streamlit as st
import time

# Page Configuration and Header
st.set_page_config(page_title="AI Agent Interface", page_icon="😁")
st.title("Hello World Interface")


# Sidebar Settings
with st.sidebar:
    st.header("Agent Configuration")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    system_prompt = st.text_area("System Prompt", "You are a helpful medical chatbot.")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


print(st.session_state)

# dictionary = {'message': "Hellow world", 'id': 3, "parts": ["greeting", "body", "conclusion", []], "messages_dict": {}}

# print(dictionary)

# Initialize Session State for Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle New User Input
if prompt := st.chat_input("Ask your agent something..."):
    # Append & Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate & Display Assistant Response
    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            time.sleep(1)
            response = f"Hello there. My temperature is {temperature} and my task is {prompt}"
            st.write(response)

    # Save assistant response
    st.session_state.messages.append({"role": "ai", "content": response})