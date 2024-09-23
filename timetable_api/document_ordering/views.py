from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication 
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

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
    
class OrderCertificateView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    @extend_schema(
        summary = "Заказ справки",
        description = "Заказ справки для студента",
        request = CertificateOrderRequestSerializer,
        responses = {
            200: OpenApiResponse(response = CertificateOrderResponseSerializer, description = "Справка заказана успешно"),
            400: OpenApiResponse(description="Произошла ошибка при валидации данных"),
            403: OpenApiResponse(description="Студент с неподтвержденным профилем не может заказывать справки"),
            404: OpenApiResponse(description = "Не найден студент с указанным ID")
        }
    )
    def post(self, request):
        serialized_request = CertificateOrderRequestSerializer(data = request.data)
        if serialized_request.is_valid():
            try:
                student = Student.objects.get(pk = serialized_request._validated_data["student_id"])
                if not student.verified:
                    return Response("Студенты с неподтвержденными профилями не могут заказывать справки", status = status.HTTP_403_FORBIDDEN)
                certificate_type = CertificateType.objects.get(pk = serialized_request._validated_data["certificate_type"])
                new_certificate = CertificateRequest.objects.create(
                    student_info = student,
                    certificate_type = certificate_type,
                    organization_full_name = serialized_request._validated_data.get("full_organization_name"),
                    voenkomat_full_name = serialized_request._validated_data.get("full_voenkomat_name"),
                    completed = False
                )
                serialized_response = CertificateOrderResponseSerializer(data = {"certificate_id": new_certificate.pk})
                new_certificate.save()
                if(serialized_response.is_valid()):
                    return Response(data = serialized_response.data, status = status.HTTP_200_OK)
                else:
                    print(serialized_response._errors)
                    return Response("Произошла внутренняя ошибка при попытке сохранения справки", status = status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Student.DoesNotExist:
                return Response(f"Студент с ID {serialized_request._validated_data["student_id"]} не найден!", status = status.HTTP_404_NOT_FOUND)
            except CertificateType.DoesNotExist:
                return Response(f"Тип справки с ID {serialized_request._validated_data["certificate_type"]} не найден!", status = status.HTTP_404_NOT_FOUND)
        else:
            return Response(data = serialized_request._errors, status = status.HTTP_400_BAD_REQUEST)