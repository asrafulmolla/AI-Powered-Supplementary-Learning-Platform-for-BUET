"""
Django management command to index course materials into the vector database.
Usage: python manage.py index_materials
"""

from django.core.management.base import BaseCommand
from courses.models import CourseMaterial
from courses.vector_store import VectorStoreService
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Index all course materials into the vector database for semantic search'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing index before indexing',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Number of documents to process in each batch',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting vector database indexing...'))
        
        try:
            # Initialize vector store
            vector_store = VectorStoreService()
            
            # Clear existing index if requested
            if options['clear']:
                self.stdout.write(self.style.WARNING('Clearing existing index...'))
                vector_store.clear_collection()
                self.stdout.write(self.style.SUCCESS('Index cleared'))
            
            # Get all course materials
            materials = CourseMaterial.objects.all()
            total_count = materials.count()
            
            if total_count == 0:
                self.stdout.write(self.style.WARNING('No course materials found to index'))
                return
            
            self.stdout.write(f'Found {total_count} course materials to index')
            
            # Prepare documents for batch processing
            batch_size = options['batch_size']
            documents = []
            indexed_count = 0
            
            # Process materials with progress bar
            for material in tqdm(materials, desc="Indexing materials", unit="doc"):
                # Combine title, description, and content for better search
                text_content = f"{material.title}\n\n"
                
                if material.description:
                    text_content += f"{material.description}\n\n"
                
                if material.text_content:
                    text_content += material.text_content
                
                # Skip if no meaningful content
                if len(text_content.strip()) < 10:
                    continue
                
                # Prepare metadata
                metadata = {
                    'title': material.title,
                    'file_type': material.file_type,
                    'topic_name': material.topic.name if material.topic else 'N/A',
                    'tags': material.tags or '',
                }
                
                # Add to batch
                documents.append({
                    'id': material.id,
                    'text': text_content,
                    'metadata': metadata
                })
                
                # Process batch when it reaches batch_size
                if len(documents) >= batch_size:
                    try:
                        vector_store.add_documents_batch(documents)
                        indexed_count += len(documents)
                        documents = []  # Clear batch
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error indexing batch: {e}')
                        )
            
            # Process remaining documents
            if documents:
                try:
                    vector_store.add_documents_batch(documents)
                    indexed_count += len(documents)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error indexing final batch: {e}')
                    )
            
            # Persist to disk
            vector_store.persist()
            
            # Show statistics
            stats = vector_store.get_collection_stats()
            
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Successfully indexed {indexed_count} documents'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'✓ Total documents in vector store: {stats["total_documents"]}'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'✓ Embedding model: {stats["model"]}'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'✓ Vector dimension: {stats["embedding_dimension"]}'
            ))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to index materials: {e}')
            )
            raise
