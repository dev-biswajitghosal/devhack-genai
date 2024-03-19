### Install required modules and set the envvar for Gemini API Key
# pip install pypdf2
# pip install chromadb
# pip install google.generativeai
# pip install langchain-google-genai
# pip install langchain
# pip install langchain_community
# pip install jupyter

# export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"

# Import Python modules
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

# Load the models
google_api_key = os.getenv("API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key=google_api_key, safety_settings=[])
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key, safety_settings=[])

# Load the PDF and create chunks
# pdf_path = "F:/project/DevHackathon-GW/Documents/rps-2023-workers-compensation-market-outlook.pdf"
pdf_path = "https://mydevhackgenai.s3.eu-north-1.amazonaws.com/rps-2023-workers-compensation-market-outlook.pdf"
loader = PyPDFLoader(pdf_path)
# text_splitter = CharacterTextSplitter(
#     separator=".",
#     chunk_size=10000,
#     chunk_overlap=50,
#     length_function=len,
#     is_separator_regex=False,
# )

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
pages = loader.load_and_split(text_splitter)

# no_of_pages = len(pages)
# Turn the chunks into embeddings and store them in Chroma
vectordb = Chroma.from_documents(pages, embeddings)

# Configure Chroma as a retriever with top_k=5
retriever = vectordb.as_retriever(search_kwargs={"k": 5})

# Create the retrieval chain
template = """
You are a helpful AI assistant.
Answer based on the context provided. 
context: {context}
input: {input}
answer:
"""
prompt = PromptTemplate.from_template(template)
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

# Invoke the retrieval chain
response = retrieval_chain.invoke(
    {"input": "Provide me 10 preventive measures for construction workers and give it in a json format."})
# print(response)
# Print the answer to the question
print(response["context"])
print(response["answer"])
