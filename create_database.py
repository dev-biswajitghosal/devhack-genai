from langchain_community.document_loaders import S3DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
S3_bucket = os.getenv("S3_BUCKET_NAME")


def load_documents(prefix):
    try:
        loader = S3DirectoryLoader(S3_bucket, prefix=prefix)
        documents = loader.load()
        return documents
    except Exception as e:
        print("Unable to load documents.", e)


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # document = chunks[25]
    # print(document.page_content)
    # print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document], prefix):
    chroma_path = f"chroma/{prefix}"
    # Clear out the database first.
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY), persist_directory=chroma_path
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {chroma_path}.")


def generate_data_store(prefix):

    try:
        documents = load_documents(prefix)
        chunks = split_text(documents)
        save_to_chroma(chunks, prefix)
        return True
    except Exception as e:
        print("Unable to generate the data store.", e)
        return False

