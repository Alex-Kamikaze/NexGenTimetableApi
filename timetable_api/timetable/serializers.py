from rest_framework import serializers
from .models import Group, Teacher, Timetable


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

class TimetableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = "__all__"

class TimetableSerializer(serializers.Serializer):
    day_of_week = serializers.IntegerField(default=0, label="День недели")
    pair_number = serializers.IntegerField(default=1, label = "Номер пары")
    distant_pair = serializers.BooleanField(default=False, label = "Пара в дистанционном формате")
    subject_name = serializers.CharField(max_length = 100, label = "Название дисциплины")
    teacher_name = serializers.CharField(max_length = 200, label = "ФИО Преподавателя")
    cabinet_number = serializers.CharField(max_length = 4, label = "Номер кабинета")
    pair_begin_time = serializers.CharField(label = "Время начала пары")
    pair_end_time = serializers.CharField(label = "Время окончания пары")
    denominator_options = serializers.CharField(max_length = 2, label = "Настройки числителя/знаменателя")

class SubstitutionRequestSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(label = "ID Группы")
    date = serializers.DateField(label = "Дата замещения")

class SubstitutionResponseSerializer(serializers.Serializer):
    date_of_substitution = serializers.DateField(label = "Дата замещения")
    pair_num = serializers.IntegerField(label = "Номер пары")
    subject = serializers.CharField(label = "Дисциплина на замещении")
    teacher = serializers.CharField(label = "Преподаватель на замещении")
    cabinet = serializers.CharField(label = "Кабинет")
    distant_pair = serializers.BooleanField(label = "Дистанционное занятие")
