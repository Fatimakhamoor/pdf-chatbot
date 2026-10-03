# 📄 Streamlit PDF Chatbot

An AI-powered chatbot that allows users to upload PDF documents and ask questions about their content.

---

## 🛠️ Tools & Tech Stack

- **Framework:** Streamlit
- **LLM Orchestration:** LangChain (`langchain-groq`)
- **Model:** Groq API (`openai/gpt-oss-120b`)
- **PDF Parser:** `pypdf`
- **Environment Control:** `python-dotenv`

---

## ⚙️ How It Works (Process)

1. **PDF Upload:** User uploads a PDF file through the Streamlit interface.
2. **Text Extraction:** `pypdf` extracts text content from the document.
3. **Query Processing:** LangChain passes the document context and user query to Groq LLM.
4. **Answer Generation:** Groq generates a fast response and displays it in the chat UI.