from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer
from django_elasticsearch_dsl.search import Search
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20  # تعداد آیتم‌های هر صفحه
    page_query_param = 'page'  # نام پارامتر مربوط به شماره صفحه در URL
    page_size_query_param = 'page_size'  # نام پارامتر مربوط به تعداد آیتم‌های هر صفحه در URL
    max_page_size = 1000  # تعداد آیتم‌های حداکثر هر صفحه


class BookListView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        #مجموع درخواست ها 
        price_range = self.request.GET.get('price_range')
        query = self.request.GET.get('query')
        ordering = self.request.GET.get('ordering')
        genre_id = self.request.GET.get('genre_id')
        birth_city_id = self.request.GET.get('birth_city_id')

        queryset = Book.objects.all()

        if query:
            # جستجو در Elasticsearch با استفاده از نمایه 'books'
            search = Search(index='books').query("multi_match", query=query, fields=['title', 'description'])
            response = search.execute()
            # بازگرداندن نتایج جستجو از Elasticsearch
            book_ids = [hit.meta.id for hit in response]
            queryset = queryset.filter(id__in=book_ids)
        
        if price_range:
            # تجزیه و تحلیل محدوده قیمت از رشته
            min_price, max_price = map(int, price_range.split(','))

            # فیلتر کردن بر اساس محدوده قیمت
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        # مرتب سازی نتایج بر اساس قیمت
        if ordering == 'price':
            queryset = queryset.order_by('price')
        elif ordering == '-price':
            queryset = queryset.order_by('-price')  #?price_range=100000,140000&ordering=price
        # فیلتر کردن بر اساس ژانر
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)
        #فیلتر کردن بر اساس محل تولد نویسنده
        if birth_city_id:
            queryset = queryset.filter(authors__birth_city_id=birth_city_id)
        #URL GET==> /?price_range=100000,140000&genre_id=1&birth_city_id=2
        return queryset
