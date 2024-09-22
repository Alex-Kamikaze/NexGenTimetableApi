from django.urls import path
from .views import *

urlpatterns = [
    path("get-certificate-types", CertificateTypeView.as_view(), name="get-certificate-types"),
    path("order-certificate", OrderCertificateView.as_view(), name="order-certificate"),
]