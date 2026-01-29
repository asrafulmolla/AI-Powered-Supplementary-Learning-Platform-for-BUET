import os
import django
import sys

# Setup Django environment
sys.path.append('e:/BUET-CSE-FEST-2026')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.rag_service import RAGService
from courses.vector_store import VectorStoreService
from courses.models import CourseMaterial

def test_ai_features():
    print("--- Starting AI & RAG Feature Validation ---")
    
    # 1. Test Vector Store
    print("\n1. Testing Vector Store (ChromaDB)...")
    try:
        vs = VectorStoreService()
        stats = vs.get_collection_stats()
        print(f"   [OK] ChromaDB active. Total documents indexed: {stats.get('total_documents')}")
        
        # Test a semantic search directly
        search_query = "sorting algorithms"
        vs_results = vs.search(search_query, n_results=2)
        print(f"   [OK] Semantic search for '{search_query}' returned {len(vs_results)} results.")
        for r in vs_results:
            title = r['metadata'].get('title', 'Unknown')
            dist = r.get('distance', 0.0)
            print(f"     - {title} (Distance: {dist:.4f})")
    except Exception as e:
        print(f"   [ERROR] Vector Store Error: {e}")

    # 2. Test RAG Service
    print("\n2. Testing RAG Service (Gemini + ChromaDB)...")
    try:
        rag = RAGService()
        query = "What are the core concepts of software engineering?"
        print(f"   - Querying: '{query}'")
        response = rag.generate_answer(query)
        print(f"   [OK] Answer received (Length: {len(response['answer'])} chars)")
        print(f"   [OK] Sources cited: {len(response['sources'])} sources found.")
    except Exception as e:
        print(f"   [ERROR] RAG Service Error: {e}")

    # 3. Test Quiz Generation
    print("\n3. Testing Quiz Generation...")
    try:
        quiz = rag.generate_quiz("Operating Systems")
        if quiz and len(quiz) > 0:
            print(f"   [OK] Quiz generated: {len(quiz)} questions found.")
            print(f"     - Example Q: {quiz[0]['question']}")
        else:
            print("   [ERR] Quiz generation returned empty results.")
    except Exception as e:
        print(f"   [ERROR] Quiz Error: {e}")

    # 4. Test Flashcard Generation
    print("\n4. Testing Flashcard Generation...")
    try:
        cards = rag.generate_flashcards("Data Structures")
        print(f"   [OK] Flashcards generated: {len(cards)} cards found.")
    except Exception as e:
        print(f"   [ERROR] Flashcard Error: {e}")

    print("\n--- Validation Complete ---")

if __name__ == "__main__":
    test_ai_features()
