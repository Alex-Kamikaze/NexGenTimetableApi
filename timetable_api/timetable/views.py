from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import *
from .models import *

class TimetablePresenterModel:
    def __init__(self, day_of_week, pair_number, distant_pair, subject_name, teacher_name, cabinet_number, pair_begin_time, pair_end_time, denominator_options):
        self.day_of_week = day_of_week
        self.pair_number = pair_number
        self.distant_pair = distant_pair
        self.subject_name = subject_name
        self.teacher_name = teacher_name
        self.cabinet_number = cabinet_number
        self.pair_begin_time = pair_begin_time
        self.pair_end_time = pair_end_time
        self.denominator_options = denominator_options

class SubstituionPresenterModel:
    def __init__(self, date_of_substitution, pair_num, subject, cabinet, teacher, distant_pair):
        self.date_of_substitution = date_of_substitution
        self.pair_num = pair_num
        self.subject = subject
        self.cabinet = cabinet
        self.teacher = teacher
        self.distant_pair = distant_pair


class GroupListView(APIView):
    @extend_schema(
        summary="Получение списка групп",
        description="Возвращает список групп из базы данных",
        responses = {
            200: OpenApiResponse(response=GroupSerializer, description="Список групп успешно получен"),
            404: OpenApiResponse(description = "Не найдено групп в базе данных")
        }
    )
    def get(self, request):
        groups_from_db = Group.objects.all()
        if len(groups_from_db) == 0:
            return Response("Не найдено учебных групп в базе данных", status = status.HTTP_404_NOT_FOUND)
        serialized_groups = GroupSerializer(groups_from_db, many = True)
        return Response(serialized_groups.data, status = status.HTTP_200_OK)
    
class TeacherView(APIView):
    @extend_schema(
        summary="Получение списка преподавателей",
        description = "Возвращает список всех преподавателей",
        responses = {
            200: OpenApiResponse(response = TeacherSerializer, description = "Список преподавателей получен успешно"),
            404: OpenApiResponse(description = "Не удалось получить список преподавателей")
        }
    )
    def get(self, request):
        teachers_from_db = Teacher.objects.all()
        if len(teachers_from_db) == 0:
            return Response("Не найдено преподавателей в базе данных", status = status.HTTP_404_NOT_FOUND)
        serialized = TeacherSerializer(teachers_from_db, many = True)

        return Response(serialized.data, status = status.HTTP_200_OK)
    
class TimetableForGroupView(APIView):
    @extend_schema(
        summary = "Получение расписания для группы",
        description = "Возвращает расписание для группы с указанными ID",
        responses = {
            200: OpenApiResponse(response = TimetableSerializer, description = "Расписание получено успешно"),
            404: OpenApiResponse(description = "Не удалось получить расписание для группы с указанным ID")
        }
    )
    def get(self, request, group_id):
        try:
            result = []
            timetable = Timetable.objects.filter(group_id=group_id)
            for pair in timetable:
                timetable_view = TimetablePresenterModel(day_of_week=pair.day_of_week, pair_number=pair.pair_number, distant_pair = pair.distant_pair, subject_name=pair.subject_id.subject_name, teacher_name=pair.teacher_id.teacher_name, cabinet_number=pair.cabinet_number, pair_begin_time=pair.pair_begin_time, pair_end_time = pair.pair_end_time, denominator_options=pair.denominator_options)
                result.append(timetable_view)

            serialized_data = TimetableSerializer(result, many=True)
            return Response(serialized_data.data, status = status.HTTP_200_OK)

        except Timetable.DoesNotExist:
            return Response(f"Не найдено расписания для группы с id {group_id}", status = status.HTTP_404_NOT_FOUND)
        
class TimetableForTeacherView(APIView):
    @extend_schema(
        summary = "Получение пар для преподавателя",
        description = "Возвращает расписание для конкретного преподавателя",
        responses = {
            200: OpenApiResponse(response = TimetableModelSerializer, description = "Расписание получено успешно"),
            400: OpenApiResponse(description = "ID Преподавателя не найдено")
        }
    )
    def get(self, request, teacher_id):
        try:
            result = []
            timetable = Timetable.objects.filter(teacher_id = teacher_id)
            if len(timetable) == 0:
                return Response(f"Не найдено пар для преподавателя с ID {teacher_id}", status = status.HTTP_400_BAD_REQUEST)
            for pair in timetable:
                timetable_view = TimetablePresenterModel(day_of_week=pair.day_of_week, pair_number=pair.pair_number, distant_pair = pair.distant_pair, subject_name=pair.subject_id.subject_name, teacher_name=pair.teacher_id.teacher_name, cabinet_number=pair.cabinet_number, pair_begin_time=pair.pair_begin_time, pair_end_time = pair.pair_end_time, denominator_options=pair.denominator_options)
                result.append(timetable_view)

            serialized_data = TimetableSerializer(result, many=True)
            return Response(serialized_data.data, status = status.HTTP_200_OK)
        except Timetable.DoesNotExist:
            return Response(f"Не найдено пар для преподавателя с ID {teacher_id}", status = status.HTTP_400_BAD_REQUEST)
        
class SubstitutionForGroup(APIView):
    @extend_schema(
        summary="Поиск замещения для группы",
        description="Возвращает список замещений для указанной группы в определенную дату",
        request = SubstitutionRequestSerializer,
        responses = {
            200: OpenApiResponse(response = SubstitutionResponseSerializer, description = "Замещения загружены успешно"),
            400: OpenApiResponse(description = "Произошла ошибка при валидации запроса")
        },
        parameters = [
            OpenApiParameter(name = "group_id", type=OpenApiTypes.INT),
            OpenApiParameter(name = "date", type = OpenApiTypes.DATE)
        ]
    )
    def get(self, request):
        request_data = SubstitutionRequestSerializer(data = request.GET)

        if request_data.is_valid():
            substitutions = Substitution.objects.filter(date_of_substitution = request_data._validated_data["date"], group_id = request_data._validated_data["group_id"])
            result = []
            for substitution in substitutions:
                result.append(SubstituionPresenterModel(date_of_substitution=substitution.date_of_substitution, pair_num=substitution.original_class.pair_number, subject = substitution.subject_on_substitution, cabinet=substitution.cabinet_on_substitution, teacher = substitution.teacher_on_substitution.teacher_name, distant_pair=substitution.distant_pair))

            serialized_data = SubstitutionResponseSerializer(result, many=True)
            return Response(serialized_data.data, status = status.HTTP_200_OK)
        
        else:
            return Response(request_data._errors, status = status.HTTP_400_BAD_REQUEST)