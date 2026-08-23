from rest_framework.decorators import action
from borrowing.services import BorrowBook, ReturnBook
from .models import BorrowRecord
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import BorrowRecordSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class BorrowRecordViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    
    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.LIBRARIAN:
            return BorrowRecord.objects.all()

        return BorrowRecord.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        book = serializer.validated_data['book']
        borrow_record = BorrowBook().borrow(user, book)
        serializer.instance = borrow_record

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        borrow_record = self.get_object()

        if borrow_record.user != request.user:
            return Response(
                {"detail": "You cannot return this book."},
                status=status.HTTP_403_FORBIDDEN
            )

        ReturnBook().return_borrowed_book(borrow_record)

        return Response({"status": "book returned"})
