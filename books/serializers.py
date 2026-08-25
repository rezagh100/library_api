from rest_framework import serializers
from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'category',
            'isbn',
            'total_copies',
            'available_copies',
        ]
        read_only_fields = ['available_copies']
        
    def validate_total_copies(self, value):
        if value < 0:
            raise serializers.ValidationError("Total copies cannot be negative.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
