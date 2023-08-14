from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.CreateAPIView,
                   generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer