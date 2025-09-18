# 📄 Financial Document Q&A Assistant

This is a web application that processes financial documents (PDF and Excel) and provides an interactive question-answering system using natural language. The application is built with Streamlit and uses a local language model (LLM) powered by Ollama to answer questions about the financial data contained within the documents.

## 📋 Requirements

- [cite_start]**Streamlit**: For the web application interface.
- [cite_start]**Ollama**: To run a local LLM for natural language processing.
- **Python Libraries**: `pandas`, `PyPDF2`, and `requests`.

## 🛠️ Setup Instructions

### 1. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone [https://github.com/NamanKr24/Soothsayer-Analytics-Assignment](https://github.com/NamanKr24/Soothsayer-Analytics-Assignment)
```

### 2. Set up Ollama

- Ensure you have Ollama installed and running on your machine.

- Pull a compatible local language model, such as llama2 or mistral. You can do this from your terminal:

```bash
ollama pull llama2
```

### 3. Install Python Dependencies

- Install all the necessary Python libraries using pip:

```bash
pip install streamlit pandas openpyxl PyPDF2 requests
```

### 4. Run the Application

- Once all dependencies are installed and Ollama is running, start the Streamlit application from your terminal:

```bash
streamlit run main.py
```

- This command will open the application in your default web browser.

## 🚀 Usage

- **Upload a Document**: Use the file upload area to select and upload a financial document in either PDF or Excel format.

- **Wait for Processing**: The application will process the document and extract relevant financial information.

- **Ask Questions**: Use the interactive chat interface to ask questions about the financial data within the document. The system uses a local language model to provide accurate responses based on the uploaded document's content.
