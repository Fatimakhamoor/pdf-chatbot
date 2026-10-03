import streamlit as st
from pdf_chat_llm import get_pdf_answer

st.set_page_config(page_title="PDF Chatbot", layout="wide")
st.title("📄 PDF Chatbot ✨")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Your PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file:
        st.success(f"✅ File loaded: {uploaded_file.name}")
        st.info(f"File size: {uploaded_file.size / 1024:.2f} KB")

# Main chat interface
if uploaded_file:
    st.write(f"**Current Document:** {uploaded_file.name}")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    question = st.chat_input("Ask a question about your PDF...")
    
    if question:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        # Get answer from LLM
        with st.chat_message("assistant"):
            with st.spinner("Analyzing document..."):
                try:
                    answer = get_pdf_answer(uploaded_file, question)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    error_msg = f"Error: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

else:
    st.info("👈 Please upload a PDF file to get started!")
    st.markdown("""
    ### How it works:
    1. **Upload** a PDF file from the sidebar
    2. **Ask** any question about the document
    3. **Get** instant AI-powered answers
    
    Powered by Groq LLM 🚀
    """)
