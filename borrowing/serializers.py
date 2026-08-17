from rest_framework import serializers
from .models import BorrowRecord

class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = '__all__'
    
    def create(self, validated_data):
        book = validated_data['book']
        user = validated_data['user']
        if book.available_copies <= 0:
            raise serializers.ValidationError("No available copies of the book.")
        
        if user.borrow_records.filter(status=BorrowRecord.StatusChoices.BORROWED).count() >= 3:
            raise serializers.ValidationError("you can`t borrow more than 3 book ")
        
        return super().create(validated_data)
