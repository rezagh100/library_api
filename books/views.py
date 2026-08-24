from rest_framework.viewsets import ModelViewSet
from .models import Book, Author, Category
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsLibrarianOrReadOnly


class BookViewSet(ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorViewSet(ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
class CategoryViewSet(ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer