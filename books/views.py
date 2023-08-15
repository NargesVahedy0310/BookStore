from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination

class BookListView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination
