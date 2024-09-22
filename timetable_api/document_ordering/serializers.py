from rest_framework import serializers
from .models import CertificateType, CertificateRequest

class CertificateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateType
        fields = "__all__"

class CertificateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateRequest
        fields = "__all__"

class CertificateOrderRequestSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(label = "ID Студента")
    certificate_type = serializers.IntegerField(label = "Тип справки")
    full_organization_name = serializers.CharField(label = "Полное название организации", required = False)
    full_voenkomat_name = serializers.CharField(label = "Полное название военкомата", required = False)
    certificate_amount = serializers.IntegerField(label = "Количество экземпляров справки")

class CertificateOrderResponseSerializer(serializers.Serializer):
    certificate_id = serializers.IntegerField(label = "ID заказанной справки")