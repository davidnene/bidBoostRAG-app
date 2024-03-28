import PyPDF2
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
import streamlit as st
import os
import re


@st.cache_data
def get_pdf_text(loaded_pdfs):
    sources = []
    documents = []
    page_contents = []

#looping thru pdfs and storing content
    for pdf in loaded_pdfs:
        loader = PyPDFLoader(pdf)
        pages = loader.load()
        pdf_name = re.search(r'[^/]+$', pdf).group(0)
        for document in pages:
            sources.append(pdf_name)
            documents.append(document)
            page_contents.append(document.page_content)
    return sources, documents, page_contents