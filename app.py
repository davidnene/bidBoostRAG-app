import streamlit as st
from dotenv import load_dotenv
from get_pdf_text import get_pdf_text
def main():
    load_dotenv()
    st.set_page_config(page_title="BidBoost RAG", page_icon=":books")
    
    st.header("BidBoost RAG")
    st.subheader("Proposals Information Retriever")
    st.text_input("What would you like to retrieve?")

    with st.sidebar:
        st.subheader("Proposals")
        pdf_docs = st.file_uploader("Upload Proposals Here and Click Process", accept_multiple_files=True)
        if st.button("process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                st.write(raw_text)
                # get the text chunks

                # create vectore store



if __name__ == '__main__':
    main()