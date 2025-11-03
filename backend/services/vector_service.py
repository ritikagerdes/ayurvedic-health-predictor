import os
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


class VectorService:
    def __init__(self):
        """Initialize vector database with ChromaDB (free, local/cloud option)"""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight, free model
        
        # Initialize ChromaDB
        persist_directory = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="ayurveda_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[str], metadata: List[Dict[str, Any]] = None):
        """Add documents to the vector database"""
        if not documents:
            return
        
        # Generate embeddings
        embeddings = self.model.encode(documents).tolist()
        
        # Generate IDs
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Add to collection
        if metadata:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadata,
                ids=ids
            )
        else:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                ids=ids
            )
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        # Generate query embedding
        query_embedding = self.model.encode([query])[0].tolist()
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                result = {
                    'document': doc,
                    'distance': results['distances'][0][i] if results['distances'] else None
                }
                if results['metadatas'] and results['metadatas'][0]:
                    result['metadata'] = results['metadatas'][0][i]
                formatted_results.append(result)
        
        return formatted_results
    
    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        return self.collection.count()
    
    def initialize_ayurveda_knowledge(self):
        """Initialize the database with Ayurvedic knowledge"""
        from data.ayurveda_corpus import get_ayurveda_documents
        
        # Check if already initialized
        if self.get_collection_count() > 0:
            print("Ayurveda knowledge base already initialized")
            return
        
        print("Initializing Ayurveda knowledge base...")
        documents = get_ayurveda_documents()
        
        # Add documents in batches
        batch_size = 50
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            docs = [d['text'] for d in batch]
            metas = [d['metadata'] for d in batch]
            self.add_documents(docs, metas)
        
        print(f"Added {len(documents)} documents to knowledge base")
    
    def search_by_condition(self, condition: str, dosha: str = None) -> List[str]:
        """Search for foods and remedies for specific health conditions"""
        query = f"{condition}"
        if dosha:
            query += f" {dosha} dosha"
        
        results = self.search(query, n_results=10)
        return [r['document'] for r in results]
    
    def get_food_properties(self, food_name: str) -> List[str]:
        """Get Ayurvedic properties of a food item"""
        query = f"properties of {food_name} taste qualities effects"
        results = self.search(query, n_results=5)
        return [r['document'] for r in results]