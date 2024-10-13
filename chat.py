import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="Dispute Tech Buddy")

with st.sidebar:
    st.title(":orange[***Dispute***] :blue[**Tech Buddy**]")
    if ("EMAIL" in st.secrets) and ("PASS" in st.secrets):
        st.success("Database Login credentials already provided!", icon=None)
        hf_email = st.secrets["EMAIL"]
        hf_pass = st.secrets["PASS"]
    else:
        hf_email = st.text_input("Enter E-mail:", type="password")
        hf_pass = st.text_input("Enter password:", type="password")
        if not (hf_email and hf_pass):
            st.warning("Please enter your credentials!")
        else:
            st.success("Proceed to entering your prompt message!", icon=None)
    st.markdown(
        "?? Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!"
    )

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)


def click_button():
    response = "User Response"
    message = {"role": "user", "content": response}
    st.write(response)
    st.session_state.messages.append(message)
	
def reset_button():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you?"}
    ]	


# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # response = generate_response(prompt, hf_email, hf_pass)
            response = "Storing unencrypted secrets in a git repository is a bad practice. For applications that require access to sensitive credentials, the recommended solution to store those credentials outside the repository - such as using a credentials file not committed to the repository or passing them as environment variables.Streamlit provides native file-based secrets management to easily store and securely access your secrets in your Streamlit app.push_pin Note"
            st.write(response)
            st.button("Reset", type="primary", on_click=reset_button)
            st.button("Say hello", on_click=click_button)
            st.text_input("Name", key="Provide Case id")

    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
