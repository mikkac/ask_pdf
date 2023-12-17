import os
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import toml
from rag_chat import RAGChat
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # read local .env file

# Load configurations
config = toml.load("config.toml")
server_config = config.get("server", {})
server_host = server_config.get("host", "127.0.0.1")
server_port = server_config.get("port", 8000)


qdrant_config = config.get("qdrant", {})
qdrant_host = qdrant_config.get("host", "qdrant")
qdrant_port = qdrant_config.get("port", 6333)

app = FastAPI()
handler = RAGChat(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    qdrant_url=f"http://{qdrant_host}:{qdrant_port}",
)


class MessageRequest(BaseModel):
    user_msg: str


@app.post("/create_embeddings")
async def create_embeddings(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # Call the create_embeddings method with the temporary file path
        handler.create_embeddings(temp_file_path)

        # Clean up: remove the temporary file
        os.remove(temp_file_path)

        return {"message": "Embeddings created successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send_message")
def send_message(request: MessageRequest):
    try:
        response = handler.send_message(request.user_msg)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=server_host, port=server_port)
