from rest_framework import serializers
from .models import StockMovement, SalesRecord, MonthlySalesReport


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = "__all__"


class SalesRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRecord
        fields = "__all__"


class MonthlySalesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlySalesReport
        fields = "__all__"
