from django.urls import path
from . import views

urlpatterns = [
    path("stock-movements/", views.StockMovementListCreateView.as_view(), name="stock-movement-list-create"),
    path("stock-movements/<uuid:uid>/", views.StockMovementDetailView.as_view(), name="stock-movement-detail"),
    
    path("sales-records/", views.SalesRecordListCreateView.as_view(), name="sales-record-list-create"),
    path("sales-records/<uuid:uid>/", views.SalesRecordDetailView.as_view(), name="sales-record-detail"),
    
    path("monthly-sales/", views.MonthlySalesReportListView.as_view(), name="monthly-sales-list"),
]
