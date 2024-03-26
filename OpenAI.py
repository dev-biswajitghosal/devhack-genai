import os
import boto3
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from create_database import generate_data_store
from datetime import datetime

load_dotenv()

openai_api = os.getenv("OPENAI_API_KEY")
aws_bucket = os.getenv("S3_BUCKET_NAME")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_access = os.getenv("AWS_ACCESS_KEY_ID")
s3 = boto3.client('s3', aws_access_key_id=aws_access, aws_secret_access_key=aws_secret)


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def generate_content_from_documents(category=None, industry=None, state=None):
    prefix = f"{category}/"
    query_text = f"Give me the safety tips for {industry} industry for {state}"
    chroma_path = f"chroma/{prefix}"
    response = generate_data_store(prefix)

    if not response:
        print("Unable to generate the data store.")
        return None

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(openai_api_key=openai_api)
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return False

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_source = []
    for source in sources:
        url = "/".join(source.split("/")[3:])
        formatted_url = f"https://mygenaidevhack.s3.amazonaws.com/{url}"
        if formatted_url not in formatted_source:
            formatted_source.append(formatted_url)
    formatted_response = {
        "response": response_text,
        "sources": formatted_source,
        "industry": industry,
        "state": state,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    url = s3.put_object(Bucket=aws_bucket, Key=f"archive/{prefix}{datetime.now()}.txt", Body=str(formatted_response))
    if url:
        return True
    return False
