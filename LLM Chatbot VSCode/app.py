import streamlit as st
import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']

# Custom CSS
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #ffe6f2;
    }
    .main-title {
        color: #FFFFFF;
        background-color: #ff66b2;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-size: 28px;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .chat-header {
        font-size: 22px;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 10px;
        text-align: center;
        border-bottom: 2px solid #ff66b2;
        padding-bottom: 10px;
    }
    .chat-message {
        font-size: 16px;
        margin-bottom: 5px;
        padding: 10px;
        border-radius: 5px;
        background-color: #ffe6f2;
        color: #2C3E50;
    }
    .chat-user {
        color: #ff66b2;
        font-weight: bold;
    }
    .chat-bot {
        color: #ff3399;
        font-weight: bold;
    }
    .input-container {
        display: flex;
        gap: 10px;
    }
    .input-box {
        flex-grow: 1;
    }
    .send-button {
        background-color: #ff66b2;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
    }
    .send-button:hover {
        background-color: #ff3399;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.markdown('<div class="main-title">Groq Chat App</div>', unsafe_allow_html=True)

    # Add customization options to the sidebar
    with st.sidebar:
        st.title('Customize Chatbot')
        model = st.selectbox('Choose a model', ['mixtral-8x7b-32768', 'llama2-70b-4096'])
        conversational_memory_length = st.slider('Conversational memory length:', 1, 10, value=5)

    memory = ConversationBufferWindowMemory(k=conversational_memory_length)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'groq_chat' not in st.session_state:
        st.session_state.groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)

    if 'conversation' not in st.session_state:
        st.session_state.conversation = ConversationChain(llm=st.session_state.groq_chat, memory=memory)

    # User input section
    with st.form(key='user_input_form'):
        user_question = st.text_input("Ask a question:", key='user_input')
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_question:
        response = st.session_state.conversation(user_question)
        message = {'human': user_question, 'AI': response['response']}
        st.session_state.chat_history.append(message)

    # Display chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">Chat History</div>', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        st.markdown(
            f"<div class='chat-message'><span class='chat-user'>You:</span> {message['human']}<br>"
            f"<span class='chat-bot'>Chatbot:</span> {message['AI']}</div>",
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
