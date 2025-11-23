"""
ChromaDB Manager for document embeddings and similarity search
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from pathlib import Path
import uuid

from .config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHROMA_DB_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SIMILARITY_THRESHOLD,
    TOP_K_RESULTS
)

class ChromaDBManager:
    """Manage ChromaDB collection for document classification"""
    
    def __init__(self):
        """Initialize ChromaDB and embedding model"""
        # Create ChromaDB directory if not exists
        CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB_DIR),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedding model (sentence-transformers)
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "OUSL document classification"}
        )
        
        print(f"ChromaDB initialized. Collection: {COLLECTION_NAME}")
        print(f"Current documents: {self.collection.count()}")
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + CHUNK_SIZE
            chunk = text[start:end]
            
            if chunk.strip():  # only add non-empty chunks
                chunks.append(chunk.strip())
            
            start += CHUNK_SIZE - CHUNK_OVERLAP
        
        return chunks
    
    def add_document(self, text: str, metadata: Dict):
        """
        Add a document to ChromaDB
        - Chunks the text
        - Creates embeddings
        - Stores in collection
        """
        # Chunk the document
        chunks = self.chunk_text(text)
        
        if not chunks:
            print(f"No valid chunks for document: {metadata.get('filename', 'unknown')}")
            return
        
        # Generate embeddings for each chunk
        embeddings = self.embedding_model.encode(chunks).tolist()
        
        # Create unique IDs for each chunk
        doc_id = str(uuid.uuid4())
        chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Prepare metadata for each chunk
        chunk_metadata = [
            {
                **metadata,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'doc_id': doc_id
            }
            for i in range(len(chunks))
        ]
        
        # Add to ChromaDB
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=chunk_metadata,
            ids=chunk_ids
        )
        
        print(f"Added {len(chunks)} chunks from: {metadata.get('filename', 'unknown')}")
    
    def add_documents_batch(self, documents: List[Dict[str, str]]):
        """
        Add multiple documents to ChromaDB
        documents: List of {text, metadata}
        """
        for doc in documents:
            self.add_document(doc['text'], doc['metadata'])
        
        print(f"Total documents in collection: {self.collection.count()}")
    
    def search_similar(self, query_text: str, n_results: int = TOP_K_RESULTS) -> List[Dict]:
        """
        Find similar documents using semantic search
        Returns list of similar chunks with metadata
        """
        # Generate embedding for query
        query_embedding = self.embedding_model.encode([query_text]).tolist()
        
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        # Format results
        similar_docs = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                similar_docs.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'similarity': 1 - results['distances'][0][i]  # convert distance to similarity
                })
        
        # Filter by similarity threshold
        similar_docs = [
            doc for doc in similar_docs 
            if doc['similarity'] >= SIMILARITY_THRESHOLD
        ]
        
        return similar_docs
    
    def reset_collection(self):
        """Delete and recreate the collection (use with caution!)"""
        self.client.delete_collection(name=COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "OUSL document classification"}
        )
        print("Collection reset successfully")
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        
        # Count documents by label
        if count > 0:
            # Sample some documents to get label distribution
            sample = self.collection.get(limit=count)
            labels = [meta.get('label', 'unknown') for meta in sample['metadatas']]
            
            from collections import Counter
            label_counts = Counter(labels)
            
            return {
                'total_chunks': count,
                'label_distribution': dict(label_counts)
            }
        
        return {'total_chunks': 0, 'label_distribution': {}}
