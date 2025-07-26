# import os
# import requests
# from bs4 import BeautifulSoup
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_pinecone import PineconeVectorStore
# from langchain_core.documents import Document  # ✅ YEH NAYI LINE IMPORT KARNI HAI
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv

# load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# INDEX_NAME = "changi-chatbot"

# def scrape_and_clean(url):
#     print(f"Scraping {url}...")
#     try:
#         response = requests.get(url, timeout=10)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         for element in soup(["script", "style", "nav", "footer"]):
#             element.decompose()
#         text = soup.get_text()
#         lines = (line.strip() for line in text.splitlines())
#         return '\n'.join(line for line in lines if line)
#     except requests.RequestException as e:
#         print(f"Error scraping {url}: {e}")
#         return ""

# print("Step 1: Starting data scraping...")
# urls = [
#     "https://www.changiairport.com/en/airport-guide/facilities-and-services.html",
#     "https://www.jewelchangiairport.com/en/attractions.html",
#     "https://www.changiairport.com/en/flights/airlines.html"
# ]
# all_text = ''.join(scrape_and_clean(url) for url in urls)

# print("\nStep 2: Chunking data...")
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
# chunks = text_splitter.split_text(all_text)
# # ✅ YEH NAYI LINE ADD KARNI HAI: Strings ko Document objects mein convert karo
# documents = [Document(page_content=chunk) for chunk in chunks]


# print("\nStep 3: Initializing embedding model...")
# embeddings_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# print("\nStep 4: Setting up Pinecone and uploading data...")
# pc = Pinecone(api_key=PINECONE_API_KEY)

# if INDEX_NAME not in pc.list_indexes().names():
#     print(f"Creating new Serverless index: {INDEX_NAME}")
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=384,
#         metric='cosine',
#         spec=ServerlessSpec(
#             cloud='aws',
#             region='us-east-1'
#         )
#     )

# # ✅ YEH LINE BADALNI HAI: 'chunks' ki jagah naye 'documents' variable ko use karo
# PineconeVectorStore.from_documents(
#     documents=documents,
#     embedding=embeddings_model,
#     index_name=INDEX_NAME
# )
# print("\n--- All Done! Data has been successfully ingested. ---")
import os
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings # ✅ Naya Import
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # ✅ Google Key Load Karo
INDEX_NAME = "changi-chatbot"

# ... (scrape_and_clean function waisa hi rahega) ...
def scrape_and_clean(url):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        return '\n'.join(line for line in lines if line)
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return ""

print("Step 1: Starting data scraping...")
urls = [
    "https://www.changiairport.com/en/airport-guide/facilities-and-services.html",
    "https://www.jewelchangiairport.com/en/attractions.html",
    "https://www.changiairport.com/en/flights/airlines.html"
]
all_text = ''.join(scrape_and_clean(url) for url in urls)

print("\nStep 2: Chunking data...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = text_splitter.split_text(all_text)
documents = [Document(page_content=chunk) for chunk in chunks]

print("\nStep 3: Initializing Google Embedding Model...")
# ✅ SentenceTransformer ki jagah Google ka model use karo
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

print("\nStep 4: Setting up Pinecone and uploading data...")
pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in pc.list_indexes().names():
    print(f"Creating new Serverless index: {INDEX_NAME}")
    pc.create_index(
        name=INDEX_NAME,
        dimension=768, # ✅ Google Embedding ka dimension 768 hota hai
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

PineconeVectorStore.from_documents(
    documents=documents,
    embedding=embeddings_model,
    index_name=INDEX_NAME
)
print("\n--- All Done! Data has been successfully ingested. ---")