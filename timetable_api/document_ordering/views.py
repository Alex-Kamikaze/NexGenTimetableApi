from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import *
from .models import *

class CertificateTypeView(APIView):
    @extend_schema(
        summary = "Список типов справок",
        description = "Возвращает список видов справок, доступных для заказа",
        responses = {
            200: OpenApiResponse(response = CertificateTypeSerializer, description = "Список типов справок получен успешно"),
            404: OpenApiResponse(description = "Не удалось найти список справок")
        }
    )
    def get(self, request):
        certificate_types = CertificateType.objects.all()
        if len(certificate_types) == 0:
            return Response("Не удалось получить список справок", status = status.HTTP_404_NOT_FOUND)
        serialized_types = CertificateTypeSerializer(certificate_types, many=True)
        return Response(data = serialized_types.data, status = status.HTTP_200_OK)
    
