from rest_framework import serializers
from .models import Group, Teacher, Timetable


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["pk", "group_name", "group_course"]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["pk", "teacher_name", "teacher_is_active"]

class TimetableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = "__all__"

class TimetableSerializer(serializers.Serializer):
    day_of_week = serializers.IntegerField(default=0)
    pair_number = serializers.IntegerField(default=1)
    distant_pair = serializers.BooleanField(default=False)
    subject_name = serializers.CharField(max_length = 100)
    teacher_name = serializers.CharField(max_length = 200)
    cabinet_number = serializers.CharField(max_length = 4)
    pair_begin_time = serializers.CharField()
    pair_end_time = serializers.CharField()
    denominator_options = serializers.CharField(max_length = 2)