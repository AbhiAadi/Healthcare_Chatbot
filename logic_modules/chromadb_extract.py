from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# persist_directory = persist_directory = "Data/Chromadata"
# user_query = "Describe about the breast cancer"

def chromadb_retreive(user_query, persist_directory):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)

    # Query the vector store
    top_n = 2
    results = vector_store.similarity_search(user_query, k=top_n)

    retrieved_data = "\n".join([result.page_content for result in results])
    return retrieved_data

# output = chromadb_retreive(user_query, persist_directory)
# print(output)