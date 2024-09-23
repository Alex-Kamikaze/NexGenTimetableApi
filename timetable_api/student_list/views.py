from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .serializers import *
from .models import *

from timetable.models import Group


class AddStudentView(APIView):
    @extend_schema(
        summary="Регистрация нового студента",
        description="Создает новый профиль студента в базе данных",
        request=StudentRegistrationRequestSerializer,
        responses = {
            200: OpenApiResponse(response = StudentRegistrationResponseSerializer, description="Студент успешно создан"),
            400:  OpenApiResponse(description = "Произошла ошибка при валидации данных")
        }
    )
    def post(self, request):
        serialized_request = StudentRegistrationRequestSerializer(data = request.data)
        if serialized_request.is_valid():
            new_user = User.objects.create_user(username = serialized_request._validated_data["student_login"], password = serialized_request._validated_data["student_password"])
            fio = serialized_request._validated_data["student_fio"].split(" ")
            new_user.first_name = fio[0]
            new_user.last_name = fio[1]
            try:
                group = Group.objects.get(pk = serialized_request._validated_data["group_id"])
                new_student = Student.objects.create(
                    user_id = new_user,
                    fio = serialized_request._validated_data["student_fio"],
                    date_of_birth = serialized_request._validated_data["date_of_birth"],
                    group_id = group
                )
                serialized_response = StudentRegistrationResponseSerializer(data = {"student_id": new_student.pk})
                new_student.save()
                if serialized_response.is_valid():
                    return Response(serialized_response.data, status = status.HTTP_200_OK)
                else:
                    return Response("Произошла внутренняя ошибка при создании профиля", status = status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Group.DoesNotExist:
                return Response(f"Не найдено группы с ID {serialized_request._validated_data["group_id"]}", status = status.HTTP_404_NOT_FOUND)

        else:
            return Response(data = serialized_request._errors, status = status.HTTP_400_BAD_REQUEST)