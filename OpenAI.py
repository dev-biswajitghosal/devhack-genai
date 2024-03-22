from langchain_openai import OpenAIEmbeddings  # Updated import statement
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.document_loaders import UnstructuredFileLoader, ImageCaptionLoader
from langchain.docstore.document import Document
from S3_bucket import download_files_from_s3  # Make sure to import this function
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API")

# Initialize ChatOpenAI model
# llm = ChatOpenAI(temperature=0, max_tokens=16000, model_name="gpt-3.5-turbo-16k", streaming=True)
os.environ["OPENAI_API_KEY"] = openai_api_key
llm = OpenAI(temperature=0)

local_directory = './tmp'
uploaded_files = download_files_from_s3(local_directory)
documents = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Get the full file path of the uploaded file
        file_path = os.path.join(os.getcwd(), uploaded_file)

        # Check if the file is an image
        if file_path.endswith((".png", ".jpg")):
            # Use ImageCaptionLoader to load the image file
            image_loader = ImageCaptionLoader(path_images=[file_path])

            # Load image captions
            image_documents = image_loader.load()

            # Append the Langchain documents to the documents list
            documents.extend(image_documents)

        elif file_path.endswith((".pdf", ".docx", ".txt")):
            # Use UnstructuredFileLoader to load the PDF/DOCX/TXT file
            loader = UnstructuredFileLoader(file_path)
            loaded_documents = loader.load()

            # Extend the main documents list with the loaded documents
            documents.extend(loaded_documents)

        # Chunk the data, create embeddings, and save in vectorstore
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        document_chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(document_chunks, embeddings)
        os.remove(file_path)

# Initialize Langchain's QA Chain with the vectorstore
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())


def generate_content_from_openAi(prompt):
    try:
        prompt = prompt + "Use the Documents to generate the content."
        result = qa({"question": prompt, "chat_history": []})
        return result['answer']
    except Exception as e:
        return str(e)
