from django.contrib import admin
from .models import StockMovement, SalesRecord, MonthlySalesReport


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("inventory", "movement_type", "quantity", "handled_by", "created_at")
    list_filter = ("movement_type", "created_at")
    search_fields = ("inventory__medicine__name", "handled_by__email")


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ("inventory", "quantity_sold", "unit_price", "total_revenue", "sold_by", "date_sold")
    list_filter = ("date_sold",)
    search_fields = ("inventory__medicine__name", "sold_by__email")


@admin.register(MonthlySalesReport)
class MonthlySalesReportAdmin(admin.ModelAdmin):
    list_display = ("month", "total_sales", "total_revenue")
    search_fields = ("month",)
