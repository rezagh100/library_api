from itsdangerous import Serializer
from rest_framework import serializers
from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "bio", "book_count"]


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "category",
            "isbn",
            "total_copies",
            "available_copies",
        ]
        read_only_fields = ["available_copies"]

    def validate_total_copies(self, value):
        if self.instance:
            borrowed_copies = (
                self.instance.total_copies
                - self.instance.available_copies
            )

            if value < borrowed_copies:
                raise serializers.ValidationError(
                    "value cannot be smaller than borrowed copies"
                )

        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
