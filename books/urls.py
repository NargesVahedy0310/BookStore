from django.urls import path, include
from rest_framework import routers
from books.views import *

router = routers.DefaultRouter()
router.register(r'book_list', BookListView, basename='book-list')
urlpatterns = [
    path('', include(router.urls)),
]
