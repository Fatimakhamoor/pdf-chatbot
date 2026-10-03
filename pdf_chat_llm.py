from dotenv import load_dotenv
import os
import pypdf
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b"
)

# Cache for storing extracted PDF text
pdf_cache = {}

def extract_pdf_text(pdf_file):
    """Extract text from uploaded PDF file or file path"""
    
    # Check if already cached
    file_id = id(pdf_file)
    if file_id in pdf_cache:
        return pdf_cache[file_id]
    
    try:
        # pypdf reads both file paths (str) and Streamlit UploadedFile streams
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted = page.extract_text()
            if extracted:
                text += f"\n--- Page {page_num + 1} ---\n"
                text += extracted
        
        # Cache the text
        pdf_cache[file_id] = text
        return text
    
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def get_pdf_answer(pdf_file, question):
    """Get answer from PDF using Groq LLM (Modern LCEL Pipe)"""
    
    try:
        # Extract text from PDF
        pdf_text = extract_pdf_text(pdf_file)
        
        # Create prompt template
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful PDF assistant. 
A user has uploaded a PDF document and is asking questions about it. 

Here is the extracted text from the document:
{context}

User Question: {question}

Answer the user's question based on the document content. 
Be accurate, concise, and helpful. 
If the information isn't in the document, say so clearly.
Provide detailed and relevant answers."""
        )
        
        # Modern LangChain Expression Language (LCEL) Chain
        chain = prompt_template | llm
        
        # Get answer
        response = chain.invoke({"context": pdf_text, "question": question})
        
        return response.content.strip()
    
    except Exception as e:
        raise Exception(f"Error processing question: {str(e)}")

if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Apni PDF file ka path yahan dein
    user_question = "What is this document about?"

    try:
        response = get_pdf_answer(pdf_path, user_question)
        print("\n--- Answer ---")
        print(response)
    except Exception as e:
        print(f"Error: {e}")