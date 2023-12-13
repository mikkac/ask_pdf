import requests
import streamlit as st
import toml
import logging

# with open(pdf_file_path, 'rb') as file:
#     response = requests.post(
#         f"{server_url}/create_embeddings",
#         files={"file": ("filename.pdf", file, "application/pdf")}
#     )
#     print("Upload Response:", response.json())

# def send_message_and_print_response(message):
#     response = requests.post(f"{server_url}/send_message", json={"user_msg": message})
#     print(f"Response to '{message}':", response.json())


# Load configurations
config = toml.load("config.toml")
server_config = config.get("server", {})
ip = server_config.get("ip", "127.0.0.1")
port = server_config.get("port", 8000)
server_url = f"http://{ip}:{port}"

st.title("Ask the PDF")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload PDF file
pdf_file = st.file_uploader("Upload a PDF file", type="pdf")
if not pdf_file:
    st.warning("Please upload a PDF file.")
    st.stop()

if pdf_file:
    with st.spinner("Uploading PDF file and creating embeddings..."):
        create_embeddings = requests.post(
            f"{server_url}/create_embeddings",
            files={"file": ("filename.pdf", pdf_file.getvalue(), "application/pdf")},
        )
        logging.info(f"Upload Response: {create_embeddings.json()}")
st.success("Done! You can ask your questions now.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
