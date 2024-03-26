import PyPDF2
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
import streamlit as st
import os



@st.cache_data
def get_pdf_text(loaded_pdfs):
    documents = []

#looping thru pdfs and storing content
    for pdf in loaded_pdfs:
        loader = PyPDFLoader(pdf)
        pages = loader.load()
        documents.extend(pages)
    return documents