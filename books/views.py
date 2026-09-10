from rest_framework.viewsets import ModelViewSet
from .models import Book, Author, Category
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsLibrarianOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Count


class BookViewSet(ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["author", "category"]
    search_fields = ["title"]


class AuthorViewSet(ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]

    queryset = Author.objects.annotate(
        book_count=Count("books")
    )

    serializer_class = AuthorSerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    