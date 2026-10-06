from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model
import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

file_path = Path(__file__).parent / "pdfs" / "Mahenjeeb_Biswal_Frontend_Engineer_Resume.pdf"
client = chromadb.HttpClient(host="localhost", port=8000)
# print(file_path)
def read_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    embeddings= OllamaEmbeddings(model="nomic-embed-text:v1.5")
    # vector_embedings = embeddings.embed_documents(split_docs)
    vectore_store = Chroma.from_documents(
        documents=chunks,
        collection_name="building_RAG",
        embedding=embeddings,
        client=client
    )
    USER_INPUT= "What are the important skills to be a good frontend engineer?"

    search_res = vectore_store.similarity_search(USER_INPUT, k=3)
    context = "\n\n".join(doc.page_content for doc in search_res)
    
    SYSTEM_PROMPT = f"""
    You are a UI/Front-End Engineer with 15 years of experience.
    Use the following context to answer the question.

    Context:
    {context}
    """
    chatbot = init_chat_model(
        model="ollama:qwen2.5:7b",
    )
    resp = chatbot.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_INPUT},
    ])
    print(resp.content)
read_pdf(file_path)