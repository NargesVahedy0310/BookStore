from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookListView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
