from django.urls import path, include

from rest_framework import routers
from books.models import *
from books.views import *

# ایجاد روتر
router = routers.DefaultRouter()
router.register(r'books', BookViewSet)

# URL های مرتبط با API
urlpatterns = [
    # ...
    path('', include(router.urls)),
    # ...
]
