from rest_framework import serializers
from .models import BorrowRecord


class BorrowRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowRecord
        exclude = ['user', 'returned_at']
        read_only_fields = ['due_date', 'status', 'borrowed_at']