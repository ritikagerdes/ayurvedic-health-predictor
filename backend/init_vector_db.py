"""
Initialize Vector Database with Ayurvedic Knowledge
Run this script once to populate the ChromaDB vector database
"""

import os
from dotenv import load_dotenv
from services.vector_service import VectorService

# Load environment variables
load_dotenv()

def main():
    print("=" * 60)
    print("Ayurvedic Health Predictor - Vector Database Initialization")
    print("=" * 60)
    print()
    
    # Initialize vector service
    print("Initializing Vector Service...")
    vector_service = VectorService()
    
    # Check if already initialized
    current_count = vector_service.get_collection_count()
    if current_count > 0:
        print(f"⚠️  Warning: Database already contains {current_count} documents.")
        response = input("Do you want to reinitialize? This will clear existing data. (yes/no): ")
        if response.lower() != 'yes':
            print("Initialization cancelled.")
            return
        
        # Clear existing collection
        print("Clearing existing collection...")
        vector_service.client.delete_collection("ayurveda_knowledge")
        vector_service.collection = vector_service.client.create_collection(
            name="ayurveda_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    
    # Initialize knowledge base
    print("\nLoading Ayurvedic knowledge corpus...")
    vector_service.initialize_ayurveda_knowledge()
    
    # Verify initialization
    final_count = vector_service.get_collection_count()
    print(f"\n✅ Successfully initialized vector database!")
    print(f"📚 Total documents: {final_count}")
    
    # Test search
    print("\n" + "=" * 60)
    print("Testing Search Functionality")
    print("=" * 60)
    
    test_queries = [
        "foods for high blood glucose",
        "Vata dosha diet recommendations",
        "liver health support"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = vector_service.search(query, n_results=2)
        for i, result in enumerate(results, 1):
            print(f"\n  Result {i}:")
            print(f"  {result['document'][:150]}...")
            if result.get('metadata'):
                print(f"  Metadata: {result['metadata']}")
    
    print("\n" + "=" * 60)
    print("✅ Vector database initialization complete!")
    print("=" * 60)
    print("\nYou can now start the backend server with:")
    print("  uvicorn main:app --reload")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        print("\nPlease check:")
        print("1. All required packages are installed (pip install -r requirements.txt)")
        print("2. CHROMA_PERSIST_DIR in .env is set correctly")
        print("3. You have write permissions to the directory")
        exit(1)