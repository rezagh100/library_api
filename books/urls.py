from .views import AuthorViewSet, BookViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('books', BookViewSet, basename='book')
router.register('authors', AuthorViewSet, basename='author')
router.register('categories', CategoryViewSet, basename='category')



urlpatterns = router.urls