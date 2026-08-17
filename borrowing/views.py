from .models import BorrowRecord
from rest_framework.viewsets import ModelViewSet
from .serializers import BorrowRecordSerializer
from rest_framework.response import Response





class BorrowRecordViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    
    
    def perform_create(self):
        queryset = BorrowRecord.object.all()
        serializer = BorrowRecordSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response()
        
        
    
    

