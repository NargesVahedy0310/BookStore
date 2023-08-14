from rest_framework import routers, viewsets
from .models import Book
from .serializers import BookSerializer

# تعریف مدل‌ویو‌ست
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

