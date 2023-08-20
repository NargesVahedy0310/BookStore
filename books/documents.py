from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Book

@registry.register_document
class BookDocument(Document):
    title = fields.TextField()
    description = fields.TextField()

    class Index:
        name = 'books'

    class Django:
        model = Book
