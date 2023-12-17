""" Streamlit app for Ask the PDF """

import logging

import requests
import streamlit as st
import toml

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
port = server_config.get("port", 8000)
server_url = f"http://server:{port}"

st.title("Ask the PDF")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_ready" not in st.session_state:
    st.session_state.file_ready = False

# Upload PDF file
pdf_file = st.file_uploader("Upload a PDF file", type="pdf")
if not pdf_file:
    st.warning("Please upload a PDF file.")
    st.stop()

if pdf_file and not st.session_state.file_ready:
    with st.spinner("Uploading PDF file and creating embeddings..."):
        create_embeddings = requests.post(
            f"{server_url}/create_embeddings",
            files={"file": ("filename.pdf", pdf_file.getvalue(), "application/pdf")},
            timeout=600,
        )
        logging.info("Upload Response: %s", create_embeddings.json())
        st.session_state.file_ready = True

st.success("Done! You can ask your questions now.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def send_message(msg):
    """Sends a message to the RAG model and returns the response."""
    resp = requests.post(
        f"{server_url}/send_message", json={"user_msg": msg}, timeout=600
    )
    logging.info("Response to '%s': %s", msg, resp.json())
    return resp


# React to user input
if prompt := st.chat_input("Ask a question"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = send_message(prompt)
    print(response.json())
    if response.status_code == 200:
        response = response.json()["response"]
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        logging.error("Error in the response! %s", response)
