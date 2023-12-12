## Ask the PDF 📖❓

<!-- <p align="center">
  <img src="https://github.com/mikkac/flashcards_generator/blob/main/resources/demo.gif?raw=true" alt="animated" />
</p> -->

## Prerequisites

- Python 3.11 or higher
- Conda (optional)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/mikkac/ask_pdf
   cd ask_pdf
   ```

2. Create a Conda environment for the project:

   ```bash
   conda create -n ask_pdf_env python=3.11
   ```

3. Activate the Conda environment:

   ```bash
   conda activate ask_pdf_env
   ```

4. Install Poetry within the Conda environment:

   ```bash
   conda install -c conda-forge poetry
   ```

5. Install project dependencies using Poetry:

   ```bash
   poetry install
   ```
6. Create a .env file in the project root directory with the following content:

    ```bash
    OPENAI_API_KEY=your_api_key_here
    ```
7. Run your project:

   ```bash
   poetry run streamlit ask_pdf/run app.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.