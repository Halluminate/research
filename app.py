import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create data directory if it doesn't exist
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)

# Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")


# Initialize or get the current session state for the conversation and documents
if 'conversation' not in st.session_state:
    st.session_state.conversation = ""
if 'documents' not in st.session_state:
    st.session_state.documents = []


# Set up the RAG components
embeddings = OpenAIEmbeddings()
# llm = ChatOpenAI(model_name='gpt-3.5-turbo')

# Initialize Groq API
model = 'llama3-8b-8192'
llm = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model
    )
    

prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")
text_splitter = RecursiveCharacterTextSplitter()

# Streamlit user interface
st.title('PDF Query Chatbot')

# Handling PDF uploads
uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=['pdf'])
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(data_dir, uploaded_file.name)
        # Save the uploaded PDF to the data directory
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        # Load and process the PDF
        pdf_loader = PyPDFLoader(file_path)
        docs = pdf_loader.load()
        documents = text_splitter.split_documents(docs)
        st.session_state.documents.extend(documents)

# If there are documents loaded, set up or update the retriever
if st.session_state.documents:
    vector = FAISS.from_documents(st.session_state.documents, embeddings)
    retriever = vector.as_retriever()
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

user_query = st.text_input("Please enter your question:", key="query_input")

if st.button("Send"):
    if user_query and 'retrieval_chain' in globals():
        response = retrieval_chain.invoke({"input": user_query})
        answer = response["answer"]
        context = response.get("context", "No specific context provided.")
        
        # Update the conversation in session state
        st.session_state.conversation += f"\nYou: {user_query}\nBot: {answer}"
        st.text_area("Conversation", value=st.session_state.conversation, height=300, disabled=True)

        if st.checkbox("Show Context"):
            st.write("Context:", context)

if st.button("Reset Conversation"):
    # Clear the session state for the conversation
    st.session_state.conversation = ""
    st.text_area("Conversation", value="", height=300, disabled=True)
    st.experimental_rerun()  # Optional: use this to refresh the input and other states
