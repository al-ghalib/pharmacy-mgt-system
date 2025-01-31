from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import StockMovement, SalesRecord, MonthlySalesReport
from .serializers import StockMovementSerializer, SalesRecordSerializer, MonthlySalesReportSerializer


class StockMovementListCreateView(generics.ListCreateAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]


class StockMovementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]


class SalesRecordListCreateView(generics.ListCreateAPIView):
    queryset = SalesRecord.objects.all()
    serializer_class = SalesRecordSerializer
    permission_classes = [IsAuthenticated]


class SalesRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalesRecord.objects.all()
    serializer_class = SalesRecordSerializer
    permission_classes = [IsAuthenticated]


class MonthlySalesReportListView(generics.ListAPIView):
    queryset = MonthlySalesReport.objects.all()
    serializer_class = MonthlySalesReportSerializer
    permission_classes = [IsAuthenticated]
