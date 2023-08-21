# from rest_framework import serializers
# from .models import Book

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    formatted_price = serializers.SerializerMethodField(method_name='format_price')
    def format_price(self, instance):
        return '{:,}'.format(instance.price)
    class Meta:
        model = Book
        fields = '__all__'
        depth = 1