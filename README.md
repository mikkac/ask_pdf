# Ask the PDF 📖❓

<p align="center">
  <img src="https://github.com/mikkac/ask_pdf/blob/main/demo/demo.gif?raw=true" alt="animated" />
</p>

## Prerequisites

- Docker and Docker Compose

## Setup Using Docker Compose

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/mikkac/ask_pdf
   cd ask_pdf
   ```

2. Create a `.env` file in the project root directory with your OpenAI API key:

    ```bash
    OPENAI_API_KEY=your_api_key_here
    ```

3. Use Docker Compose to build and run the application:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images for the project and start the containers as defined in your `docker-compose.yml` file.

4. Once the containers are up and running, you can access the application:
   
   - Streamlit App: Open `http://localhost:8501` in your browser (or the port you configured in `docker-compose.yml`).
   - FastAPI Server: Available at `http://localhost:8000` (or the port you configured in `docker-compose.yml`).

## Stopping the Application

To stop the application, you can use the following command in the terminal:

```bash
docker-compose down
```

This will stop and remove the containers and networks created by `docker-compose up`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.