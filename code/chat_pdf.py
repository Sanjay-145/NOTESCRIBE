import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores.faiss import FAISS
from InstructorEmbedding import INSTRUCTOR
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.chat_models.openai import ChatOpenAI
from htmlTemplates import css, bot_template, user_template
from langchain.llms.huggingface_hub import HuggingFaceHub

import json
from streamlit_lottie import st_lottie



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
       separator="\n",
       chunk_size=1000,
       chunk_overlap=200,
       length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
   embeddings = OpenAIEmbeddings()
   vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
   return vectorstore

def get_conversation_chain(vectorstore):
   llm = ChatOpenAI()
   memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
   conversation_chain = ConversationalRetrievalChain.from_llm(
      llm=llm,
      retriever=vectorstore.as_retriever(),
      memory=memory
   )
   return conversation_chain
   

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
   

def main(): 
    load_dotenv()
    st.write(css, unsafe_allow_html=True)

    #Animation
    # Load Lottie animation
    def load_lottiefile(filepath:str):
        with open(filepath,"r") as f:
            return json.load(f)
            
    lottie_chat = load_lottiefile("D:\\Projects\\pdf3\\templates\\Insight_anim.json")

    # Display Lottie animation (logo) 
    st.markdown(
        """
        <style>
        .logo-container {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 100px; /* Adjust the width as needed */
            height: 100px; /* Adjust the height as needed */
        }
        </style>
        """
    , unsafe_allow_html=True)

    # Add a container div with the logo-container class
    st.markdown("<div class='logo-container'></div>", unsafe_allow_html=True)
        
    # Display the Lottie animation inside the container
    st_lottie(lottie_chat, quality="high", width=100, height=100)
    

    # Add custom CSS for styling
    st.markdown(
        """
        <style>
            .header-text {
                font-size: 36px;
                color: #1E90FF;
                margin-bottom: 20px;
            }
            .subheader-text {
                font-size: 24px;
                color: #2E8B57;
                margin-bottom: 10px;
            }
            .button-primary {
                background-color: #1E90FF;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
            .button-primary:hover {
                background-color: #0066CC;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("Welcome to NoteScribe!")
    st.subheader("Gain Insights Effortlessly")
    st.markdown(
        """
        <p style="font-family: 'Verdana', sans-serif; font-size: 24px; font-weight: bold; color: #1E90FF;">Unleash the Power of Your PDFs!</p>
        <p style="font-family: 'Verdana', sans-serif; font-size: 18px;">Upload your PDFs, Ask Questions, and Uncover Valuable Insights Instantly</p>
        """,
        unsafe_allow_html=True
    )


    #contents
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)
    
    st.subheader("Your Documents")
    pdf_docs = st.file_uploader(
         "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    if st.button("Process"):
        with st.spinner("Processing"):

            # Get the PDF text
            raw_text = get_pdf_text(pdf_docs)
            
            # Get the text chunks
            text_chunks = get_text_chunks(raw_text)
            
            # Create vector base
            vectorstore = get_vectorstore(text_chunks)

            # Create conversation chain
            st.session_state.conversation = get_conversation_chain(vectorstore)
   
