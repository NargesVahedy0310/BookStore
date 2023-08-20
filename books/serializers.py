from rest_framework import serializers
from .models import Book
# from .book_index import BookDocument
# from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# class BookDocumentSerializers(DocumentSerializer):
#     class Meta:
#         model = BookDocument
#         document = BookDocument

#         fields = ('description',)

#     def get_location(self, obj):
#         try:
#             return obj.location.to_dict()
#         except:
#             return {}
