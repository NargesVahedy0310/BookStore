from django.urls import path
from books.views import *


urlpatterns = [
    path('book_list/', BookListView.as_view()),
    path('book_list/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

]

