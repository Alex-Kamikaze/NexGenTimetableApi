from django.urls import path
from .views import *

urlpatterns = [
    path("get-certificate-types", CertificateTypeView.as_view(), name="get-certificate-types"),
]