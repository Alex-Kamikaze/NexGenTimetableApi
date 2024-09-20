from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *

class TimetableView:
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


# Create your views here.
@api_view(["GET"])
def get_group_list(request):
    groups_from_db = Group.objects.all()
    if len(groups_from_db) == 0:
        return Response("Не найдено учебных групп в базе данных", status = status.HTTP_404_NOT_FOUND)
    serialized_groups = GroupSerializer(groups_from_db, many = True)
    return Response(serialized_groups.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_all_teachers(request):
    teachers_from_db = Teacher.objects.all()
    if len(teachers_from_db) == 0:
        return Response("Не найдено преподавателей в базе данных", status = status.HTTP_404_NOT_FOUND)
    serialized = TeacherSerializer(teachers_from_db, many = True)

    return Response(serialized.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_timetable_for_group(request, group_id):
    try:
        result = []
        timetable = Timetable.objects.filter(group_id=group_id)
        for pair in timetable:
            timetable_view = TimetableView(day_of_week=pair.day_of_week, pair_number=pair.pair_number, distant_pair = pair.distant_pair, subject_name=pair.subject_id.subject_name, teacher_name=pair.teacher_id.teacher_name, cabinet_number=pair.cabinet_number, pair_begin_time=pair.pair_begin_time, pair_end_time = pair.pair_end_time, denominator_options=pair.denominator_options)
            result.append(timetable_view)

        serialized_data = TimetableSerializer(result, many=True)
        return Response(serialized_data.data, status = status.HTTP_200_OK)

    except Timetable.DoesNotExist:
        return Response(f"Не найдено расписания для группы с id {group_id}", status = status.HTTP_404_NOT_FOUND)
    