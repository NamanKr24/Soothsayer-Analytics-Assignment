import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import requests
import json
import logging

# Set Streamlit page configuration
st.set_page_config(page_title="Financial Document Q&A Assistant", layout="wide")

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

# Configuration for the Ollama server
OLLAMA_API_URL = "http://localhost:11434/api/generate"
# You might need to change the model name to one you have pulled locally, e.g., 'mistral', 'llama2', 'gemma:2b'
OLLAMA_MODEL = "llama2" 

# --- Utility Functions ---

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file.
    Note: This is a basic text extraction and may not be sufficient for complex financial documents.
    A more robust solution would involve table and layout detection.
    """
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        logging.error(f"Error extracting PDF: {e}")
        st.error(f"Error processing PDF file: {e}")
        return None

def extract_data_from_excel(file):
    """
    Extracts data from the first sheet of an Excel file into a string.
    """
    try:
        # Read all sheets into a dictionary of DataFrames
        xls = pd.ExcelFile(file)
        data = ""
        # Iterate over all sheets to extract data
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet_name)
            data += f"\n--- Sheet: {sheet_name} ---\n"
            data += df.to_string(index=False)
        return data
    except Exception as e:
        logging.error(f"Error extracting Excel: {e}")
        st.error(f"Error processing Excel file: {e}")
        return None

def call_ollama_api(prompt, model):
    """
    Sends a request to the Ollama API to generate a response.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False # Disable streaming for a single, complete response
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Return the generated response text
        if "response" in data:
            return data["response"]
        else:
            return "No response text found in the API response."
            
    except requests.exceptions.RequestException as e:
        logging.error(f"API call to Ollama failed: {e}")
        st.error(f"Could not connect to Ollama. Please ensure it is running and the model '{model}' is available.")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from Ollama API: {e}")
        st.error("Failed to process the response from the language model.")
        return None

# --- Main Streamlit Application ---

st.title("📄 Financial Document Q&A Assistant")
st.markdown("Upload a financial document (PDF or Excel) and ask questions about its content. Make sure Ollama is running locally with a model like `llama2` or `mistral`.")

# Initialize session state variables
if "document_content" not in st.session_state:
    st.session_state.document_content = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# File uploader section
uploaded_file = st.file_uploader("Upload a financial document", type=["pdf", "xlsx"], key="file_uploader")

# Display the content of the uploaded document in an expander
if uploaded_file is not None:
    if uploaded_file.name.endswith('.pdf'):
        st.session_state.document_content = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        st.session_state.document_content = extract_data_from_excel(uploaded_file)
    
    # Check if content was successfully extracted
    if st.session_state.document_content:
        with st.expander("Uploaded Document Content"):
            st.text_area("Content", st.session_state.document_content, height=300)

        # Display a status message
        st.success("Document processed successfully! You can now ask questions.")
        st.markdown("---")
        
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input in the chat
if user_prompt := st.chat_input("Ask a question about the document..."):
    # Check if a document has been uploaded and processed
    if st.session_state.document_content is None:
        st.warning("Please upload a financial document first.")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate a prompt for the language model
        full_prompt = (
            "You are a financial analyst assistant. Your task is to answer questions about the provided financial document. "
            "Use only the information from the document content below. If the information is not present, "
            "state that you cannot find the answer in the document.\n\n"
            f"Financial Document Content:\n---\n{st.session_state.document_content}\n---\n\n"
            f"User Question: {user_prompt}"
        )
        
        # Get response from the language model
        with st.spinner("Thinking..."):
            ollama_response = call_ollama_api(full_prompt, OLLAMA_MODEL)
            
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(ollama_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ollama_response})