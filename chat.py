import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="Dispute Tech Buddy")

with st.sidebar:
    st.title(":orange[***Dispute***] :blue[**Tech Buddy**]")
    hf_username=""
    hf_pass=""
    hf_dbname=""
    if ("username" in st.secrets) and ("password" in st.secrets) and ("database" in st.secrets):
        st.success("Database Login credentials already provided!", icon=None)
        hf_username = st.secrets["username"]
        hf_pass = st.secrets["password"]
        hf_dbname = st.secrets["database"]
    else:
        hf_username = st.text_input("Enter DB Username:", type="default")
        hf_pass = st.text_input("Enter DB Password:", type="password")
        hf_dbname = st.text_input("Enter DB Name:", type="default")

    if not (hf_username and hf_pass and hf_dbname):
        st.warning("Please enter your DB credentials!")
    else:
        # Initialize connection.
        #conn = st.connection('mysql', type='sql')
        conn = st.connection(name="sa", dialect = "mysql", host = "localhost", port = 3306, database = hf_dbname, username = hf_username, password = hf_pass, type='sql')

        # Perform query.
        df = conn.query('SELECT * from beneficiary;', ttl=600)

        # Print results.
        for row in df.itertuples():
            st.write(f"{row.first_name} has a :{row.last_name}:")
		
        st.success("Proceed to entering your prompt message!"+hf_username+hf_pass+hf_dbname, icon=None)
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
if prompt := st.chat_input(disabled=not (hf_username and hf_pass and hf_dbname)):
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
