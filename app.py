import streamlit as st
from dotenv import load_dotenv
from get_pdf_text import get_pdf_text
from get_text_chunks import get_text_chunks
from get_vector_store import get_vector_store
from get_converstation_chain import get_conversation_chain
from file_converter import file_converter
from upload_files import upload_files
from create_folder import create_folder
from pdf_data_store import pdf_token_pages
import pandas as pd

from htmlTemplates import css, bot_template, user_template
import os

def handle_user_question(user_question):
        st.session_state.response = st.session_state.conversation({"question": user_question})
        st.session_state.chat_history = st.session_state.response['chat_history']

        for i,message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
def handle_history():
    if st.session_state.chat_history:
        for i,message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    UPLOAD_DIRECTORY = 'docs/proposals/'

    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    loaded_pdfs = [os.path.join(UPLOAD_DIRECTORY, fname) for fname in os.listdir(UPLOAD_DIRECTORY)]
    load_dotenv()
    st.set_page_config(page_title="BidBoost RAG", page_icon=":books")
    
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("BidBoost RAG")
    st.subheader("Proposals Information Retriever")

    user_question = st.text_input("What would you like to retrieve?")
    if st.button('Clear chat'):
        st.session_state.response = None
        st.session_state.chat_history = None

    if user_question:
        try:
            handle_user_question(user_question)
        except:
            st.warning("Please upload and process proposals", icon='⚠️')
    else:
        handle_history()

    with st.sidebar:
        st.subheader("Proposals")

        st.header("Manage Proposal Documents")
        collections = ["Collection 1", "Collection 2"]  # Define your collections
        for collection in collections:
            with st.expander(f"Manage {collection}"):
                create_folder_button = st.button(f"Create {collection} Folder", key=f"create_{collection}")
                if create_folder_button:
                    create_folder(collection)
                upload_files(collection)

        pdf_docs = st.file_uploader("Upload Proposals Here and Click Process", accept_multiple_files=True)
        if st.button("process"):
            with st.spinner("Processing"):
                # save pdf files
                loaded_pdfs = file_converter(pdf_docs, UPLOAD_DIRECTORY)
                # get pdf text
                raw_docs = get_pdf_text(loaded_pdfs)
                
                #generate token data
                pdf_data = pdf_token_pages(loaded_pdfs)
                pdf_df = pd.DataFrame(pdf_data)
                pdf_df.to_csv('data/viz.csv')

                # get the text chunks
                token_chunks = get_text_chunks(raw_docs)
    
                # create vectore store
                vector_store = get_vector_store(token_chunks)

                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vector_store)
                st.success('Proposals Succesfully Processed!', icon="✅")
    
    


if __name__ == '__main__':
    main()