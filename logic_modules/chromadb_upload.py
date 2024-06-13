from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# contents =  "Data\Oncology.pdf"
# filename = "Oncology.pdf"
# persist_directory = "Data/Chromadata"
# text = process_file(contents, filename)


def chromadb_load(text, persist_directory):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_text(text)

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(docs, embedding_model, persist_directory=persist_directory)

    # Save the vector store
    vector_store.persist()
