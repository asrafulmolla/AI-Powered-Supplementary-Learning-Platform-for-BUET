import os
# Disable ChromaDB telemetry before it's even imported
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from django.conf import settings
import os
from typing import List, Dict, Any
import logging

# Suppress noisy ChromaDB telemetry loggers
logging.getLogger('chromadb.telemetry').setLevel(logging.CRITICAL)
logging.getLogger('chromadb.telemetry.product.posthog').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    Manages vector embeddings and semantic search using ChromaDB.
    """
    
    def __init__(self):
        """Initialize ChromaDB client and embedding model."""
        # Set up ChromaDB persistent directory
        self.chroma_dir = os.path.join(settings.BASE_DIR, 'chroma_db')
        os.makedirs(self.chroma_dir, exist_ok=True)
        
        # Initialize ChromaDB client with persistent storage
        # Disable anonymized telemetry to stop the capture() argument errors
        self.client = chromadb.PersistentClient(
            path=self.chroma_dir,
            settings=chromadb.Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model (lightweight and fast)
        # Using all-MiniLM-L6-v2: 384 dimensions, good balance of speed and quality
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self.embedding_model = None
        
        # Get or create collection for course materials
        try:
            self.collection = self.client.get_or_create_collection(
                name="course_materials",
                metadata={"description": "BUET course materials with semantic embeddings"}
            )
            logger.info(f"Collection initialized with {self.collection.count()} documents")
        except Exception as e:
            logger.error(f"Failed to initialize collection: {e}")
            self.collection = None
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for a given text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        if not self.embedding_model:
            raise ValueError("Embedding model not initialized")
        
        try:
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def add_document(self, doc_id: str, text: str, metadata: Dict[str, Any] = None):
        """
        Add a single document to the vector store.
        
        Args:
            doc_id: Unique identifier for the document
            text: Document text content
            metadata: Optional metadata dictionary
        """
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            # Generate embedding
            embedding = self.generate_embedding(text)
            
            # Add to collection
            self.collection.add(
                ids=[str(doc_id)],
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata or {}]
            )
            logger.debug(f"Added document {doc_id} to vector store")
        except Exception as e:
            logger.error(f"Error adding document {doc_id}: {e}")
            raise
    
    def add_documents_batch(self, documents: List[Dict[str, Any]]):
        """
        Add multiple documents to the vector store in batch.
        
        Args:
            documents: List of dicts with keys: 'id', 'text', 'metadata'
        """
        if not self.collection or not documents:
            return
        
        try:
            ids = [str(doc['id']) for doc in documents]
            texts = [doc['text'] for doc in documents]
            metadatas = [doc.get('metadata', {}) for doc in documents]
            
            # Generate embeddings in batch (more efficient)
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            embeddings_list = [emb.tolist() for emb in embeddings]
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                documents=texts,
                metadatas=metadatas
            )
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents batch: {e}")
            raise
    
    def search(self, query: str, n_results: int = 10, filter_metadata: Dict = None) -> List[Dict[str, Any]]:
        """
        Perform semantic similarity search.
        
        Args:
            query: Search query text
            n_results: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of dictionaries with keys: 'id', 'text', 'metadata', 'distance'
        """
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            # Check actual document count to avoid warnings
            total_docs = self.collection.count()
            if total_docs == 0:
                return []
            
            actual_n = min(n_results, total_docs)
            
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            
            # Perform similarity search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=actual_n,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][i],
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    })
            
            logger.debug(f"Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    def update_document(self, doc_id: str, text: str, metadata: Dict[str, Any] = None):
        """
        Update an existing document in the vector store.
        
        Args:
            doc_id: Document ID to update
            text: New text content
            metadata: New metadata
        """
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            # Delete old version
            self.delete_document(doc_id)
            
            # Add new version
            self.add_document(doc_id, text, metadata)
            logger.debug(f"Updated document {doc_id}")
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {e}")
            raise
    
    def delete_document(self, doc_id: str):
        """
        Delete a document from the vector store.
        
        Args:
            doc_id: Document ID to delete
        """
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            self.collection.delete(ids=[str(doc_id)])
            logger.debug(f"Deleted document {doc_id}")
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            raise
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        if not self.collection:
            return
        
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(name="course_materials")
            self.collection = self.client.create_collection(
                name="course_materials",
                metadata={"description": "BUET course materials with semantic embeddings"}
            )
            logger.info("Collection cleared")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            raise
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store collection.
        
        Returns:
            Dictionary with collection statistics
        """
        if not self.collection:
            return {"error": "Collection not initialized"}
        
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": "course_materials",
                "embedding_dimension": 384,  # all-MiniLM-L6-v2
                "model": "all-MiniLM-L6-v2"
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"error": str(e)}
    
    def persist(self):
        """
        Persist is handled automatically in ChromaDB 0.4+.
        This method is kept for backward compatibility with the interface.
        """
        logger.info("ChromaDB automatically handles persistence in versions 0.4+")
