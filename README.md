# AI CV Builder

This project is an AI-powered CV builder that generates professional summaries and LaTeX-formatted CVs using Google's Gemini API.

## Prerequisites

Before running the project, ensure you have the following installed:

1.  **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2.  **LaTeX Distribution**: You need `pdflatex` to generate PDFs.
    *   **Windows**: [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/)
    *   **macOS**: MacTeX
    *   **Linux**: `sudo apt-get install texlive-full`

## Prerequisites

1.  **Python 3.10+**
2.  **Google Gemini API Key**
3.  **LaTeX Distribution (Required for PDF Generation)**
    *   The application uses `pdflatex` to generate the PDF CV.
    *   **Windows**: Install [MiKTeX](https://miktex.org/download).
        *   Download the installer and run it.
        *   During installation, choose "Install missing packages on-the-fly" -> "Yes" (recommended) or "Ask me first".
        *   **Important**: After installation, restart your terminal/command prompt (or VS Code) so that `pdflatex` is added to your PATH.
    *   **Mac**: Install MacTeX (`brew install --cask mactex`).
    *   **Linux**: Install TeX Live (`sudo apt-get install texlive-full`).

## Installation


1.  **Clone the repository** (if you haven't already).
2.  **Navigate to the project directory**:
    ```bash
    cd "path/to/project"
    ```
3.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Ensure you have a `.env` file in the root directory.
2.  Add your Google Gemini API key to the `.env` file:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

## Running the Application

1.  **Start the Flask server**:
    ```bash
    python backend/app.py
    ```
2.  **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

1.  Fill in your personal details and experience in the form.
2.  Paste the job offer description you are applying for.
3.  Click "Generate Summary" to get an AI-tailored professional summary.
4.  Click "Generate CV" to create and download your CV as a PDF.
