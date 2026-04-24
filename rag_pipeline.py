import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import uuid
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")


class RAG_Pipeline:
    def __init__(self):
        self.file_path = "pdf"
        self.persistent_path = "./chromadb"
        self.collection_name = "pdf_docs"

        os.makedirs(self.file_path,exist_ok=True)

        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.llm = ChatGroq(
            groq_api_key = api_key,
            model = "llama-3.1-8b-instant",
            temperature = 0.2,
            max_tokens = 1024
        )

        self.client = chromadb.PersistentClient(self.persistent_path)
        self.collection = self.client.get_or_create_collection(self.collection_name)

    def load_data(self):

        documents = []

        for filename in os.listdir(self.file_path):
            if filename.lower().endswith(".pdf"):
                complete_path = os.path.join(self.file_path,filename)
                loader = PyPDFLoader(complete_path)
                doc = loader.load()
                print(f"file successfully loaded {filename}")

                documents.extend(doc)

        return documents
        

    def chunk_data(self,docs):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50
        )

        return splitter.split_documents(docs)
        

    def create_database(self,chunks):

        if self.collection.count() == 0:

            text = [doc.page_content for doc in chunks]
            metas = [doc.metadata for doc in chunks]

            embedding = self.embedding_model.encode(text).tolist()

            self.collection.add(
                documents = text,
                embeddings = embedding,
                metadatas = metas,
                ids = [str(uuid.uuid4()) for _ in range(len(text))]
            )

            print("DB Created Successfully")
            
        else:

            print("DB already exists")

        return self.collection.count()

    def add_pdf(self,file_path):

        loader = PyPDFLoader(file_path)
        docs = loader.load()

        chunks = self.chunk_data(docs)

        text = [doc.page_content for doc in chunks]

        metas = [doc.metadata for doc in chunks]

        embedding = self.embedding_model.encode(text).tolist()
        
        self.collection.add(
            documents = text,
            embeddings = embedding,
            metadatas = metas,
            ids = [str(uuid.uuid4()) for _ in range(len(text))]
        )

        return self.collection.count()
        

    def query(self,question,top_k = 5):

        query_embedding = self.embedding_model.encode([question]).tolist()

        results = self.collection.query(
            query_embeddings = query_embedding,
            n_results = top_k
        )

        if not results["documents"] or not results["documents"][0]:
            return "No data available. Please upload a PDF first."


        doc = results["documents"][0]
        meta = results["metadatas"][0]

        if not doc:
            return "No relevant context found"
            
        context_text = []

        for i in range(len(doc)):
            source = meta[i].get("source","unknown")
            text = doc[i]

            context_text.append(f"source {source}\n {text}")

        context = "\n\n".join(context_text)

        prompt = f"""
            Use the context below and answer the question.
            If the answer is not found, say "I don't know."

            Context:
            {context}

            Question:
            {question}
            """

        response = self.llm.invoke(prompt)

        return response.content
        
    def run(self):
        docs = self.load_data()

        if docs:
            chunks = self.chunk_data(docs)
            self.create_database(chunks)