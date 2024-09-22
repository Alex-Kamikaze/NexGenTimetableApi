from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

class AddStudentView(APIView):
    @extend_schema(
        summary="Регистрация нового студента",
        description="Создает новый профиль студента в базе данных",
        responses = {
            200: OpenApiResponse(description="Студент успешно создан")
        }
    )