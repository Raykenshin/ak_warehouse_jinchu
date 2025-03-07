from django.urls import path
from .views import scan_barcode, wms_update

urlpatterns = [
    path('scan/', scan_barcode, name='scan_barcode'),
    path('update/<str:barcode>/', wms_update, name='wms_update'),
]