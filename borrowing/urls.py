from rest_framework.routers import DefaultRouter
from .views import BorrowRecordViewSet


router = DefaultRouter()

router.register('borrow-records',BorrowRecordViewSet,basename='borrow-records')

urlpatterns = router.urls
