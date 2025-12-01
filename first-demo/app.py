import streamlit as st
import os
from openai import OpenAI

st.set_page_config(
    page_title="Kebayoran Technologies - AI Demo",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Kebayoran Technologies AI Demo")
st.markdown("---")

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        st.stop()
    return OpenAI(api_key=api_key)

client = get_openai_client()

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    model = st.selectbox(
        "Select Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
        index=0
    )
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=50,
        max_value=2000,
        value=500,
        step=50
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1
    )

# Main interface
st.header("Chat with AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Check if this is an error message and display appropriately
        if message.get("is_error", False):
            st.error(message["content"])
            if "error_details" in message:
                with st.expander("Error Details"):
                    st.code(message["error_details"])
        else:
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        is_error = False
        error_details = None
        
        try:
            # Create a chat completion - exclude error messages from context
            valid_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if not m.get("is_error", False)
            ]
            stream = client.chat.completions.create(
                model=model,
                messages=valid_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
            )
            
            # Stream the response
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            is_error = True
            error_details = str(e)
            st.error(f"Error calling OpenAI API: {error_details}")
            full_response = "Sorry, I encountered an error while processing your request."
            message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history with error flag if applicable
    message_entry = {"role": "assistant", "content": full_response}
    if is_error:
        message_entry["is_error"] = True
        if error_details:
            message_entry["error_details"] = error_details
    st.session_state.messages.append(message_entry)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Powered by <a href='https://www.kebayorantechnologies.com' target='_blank'>Kebayoran Technologies</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
