from rest_framework import generics, viewsets
from .models import Book
from .serializers import *
# from rest_framework.pagination import PageNumberPagination
from django_elasticsearch_dsl.search import Search
from django.shortcuts import render
from django.http import JsonResponse
from .documents import BookDocument

class BookListView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    # pagination_class = PendingDeprecationWarning
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            # جستجو در Elasticsearch با استفاده از نمایه 'books'
            search = Search(index='books').query("multi_match", query=query, fields=['title', 'description'])
            response = search.execute()
            # بازگرداندن نتایج جستجو از Elasticsearch
            book_ids = [hit.meta.id for hit in response]
            books = Book.objects.filter(id__in=book_ids)
            return books
        return Book.objects.all()
