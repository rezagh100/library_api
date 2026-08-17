# from django.shortcuts import render
from .models import BorrowRecord
# from accounts.models import User
# from books.models import Book,Category,Author
from rest_framework.viewsets import ModelViewSet
from .serializers import BorrowRecordSerializer

class BorrowRecordViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    

