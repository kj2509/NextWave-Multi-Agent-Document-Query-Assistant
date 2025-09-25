import os


from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

UPLOAD_DIR = "uploads"

def get_retriever():
    docs = []
    for filename in os.listdir(UPLOAD_DIR):
        path = os.path.join(UPLOAD_DIR, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif filename.endswith(".txt"):
            loader = TextLoader(path)
        elif filename.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(path)
        else:
            continue

        docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
)
    documents = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = FAISS.from_documents(documents, embeddings)
    return vectordb.as_retriever(search_kwargs={"k": 5})

    #return vectordb.as_retriever()
