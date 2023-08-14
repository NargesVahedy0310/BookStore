# در فایل urls.py اپلیکیشن admin
from django.contrib import admin
from .models import Book, Author, Genre, City

# اضافه کردن دسترسی به مدل‌ها در پنل ادمین
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(City)
