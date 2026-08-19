from rest_framework import serializers
from .models import BorrowRecord


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        exclude = ["user", "returned_at","due_date"]
        read_only_fields = ["status"]