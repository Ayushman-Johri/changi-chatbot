# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_pinecone import PineconeVectorStore
# from langchain.chains import RetrievalQA
# from dotenv import load_dotenv

# load_dotenv()
# INDEX_NAME = "changi-chatbot"

# def get_chatbot_chain():
#     embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash-latest",
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         temperature=0.1,
#         convert_system_message_to_human=True
#     )

#     vectorstore = PineconeVectorStore.from_existing_index(
#         index_name=INDEX_NAME,
#         embedding=embeddings
#     )

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
#         return_source_documents=True
#     )

#     return qa_chain

# chatbot_chain = get_chatbot_chain()

# def get_answer(query: str):
#     response = chatbot_chain.invoke({"query": query})
#     return response
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings # ✅ Naya Import
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()
INDEX_NAME = "changi-chatbot"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # ✅ Google Key Load Karo

def get_chatbot_chain():
    # ✅ SentenceTransformer ki jagah Google ka model use karo
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.1,
        convert_system_message_to_human=True
    )

    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=embeddings
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
        return_source_documents=True
    )
    return qa_chain

chatbot_chain = get_chatbot_chain()

def get_answer(query: str):
    response = chatbot_chain.invoke({"query": query})
    return response