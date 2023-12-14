# Use an official Python runtime as a parent image
FROM python:3.11

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /ask_pdf

# Copy pyproject.toml and optionally poetry.lock (if exists)
COPY pyproject.toml poetry.lock* .env config.toml /ask_pdf/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of your application's code
COPY ask_pdf /ask_pdf/

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501
