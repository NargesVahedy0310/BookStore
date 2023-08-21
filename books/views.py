from rest_framework import generics, viewsets
from .models import Book
from .serializers import *
from django_elasticsearch_dsl.search import Search
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

class BookListView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        query = self.request.GET.get('query')

        queryset = Book.objects.all()

        if query:
            # جستجو در Elasticsearch با استفاده از نمایه 'books'
            search = Search(index='books').query("multi_match", query=query, fields=['title', 'description'])
            response = search.execute()
            # بازگرداندن نتایج جستجو از Elasticsearch
            book_ids = [hit.meta.id for hit in response]
            queryset = queryset.filter(id__in=book_ids)
        
        if min_price is not None:
            try:
                min_price = float(min_price)  # تبدیل به عدد اعشاری
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                return Response({'error': 'min_price باید یک مقدار عددی باشد.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if max_price is not None:
            try:
                max_price = float(max_price)  # تبدیل به عدد اعشاری
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                return Response({'error': 'max_price باید یک مقدار عددی باشد.'}, status=status.HTTP_400_BAD_REQUEST)

        return queryset
