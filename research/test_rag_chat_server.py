import requests

server_url = "http://127.0.0.1:8000"

pdf_file_path = "path/to/your/file.pdf"

with open(pdf_file_path, 'rb') as file:
    response = requests.post(f"{server_url}/create_embeddings", files={"file": file})
    print("Upload Response:", response.json())

def send_message_and_print_response(message):
    response = requests.post(f"{server_url}/send_message", json={"user_msg": message})
    print(f"Response to '{message}':", response.json())

send_message_and_print_response("What is the main topic of the uploaded document?")
send_message_and_print_response("Can you summarize the key points?")
send_message_and_print_response("What are the conclusions drawn in the document?")
