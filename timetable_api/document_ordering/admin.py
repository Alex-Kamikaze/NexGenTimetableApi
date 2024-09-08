from django.contrib import admin
from .models import CertificateRequest, CertificateType

# Register your models here.
admin.site.register(CertificateType)
admin.site.register(CertificateRequest)