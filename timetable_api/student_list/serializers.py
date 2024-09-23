from rest_framework import serializers

class StudentRegistrationRequestSerializer(serializers.Serializer):
    student_fio = serializers.CharField(label = "ФИО Студента")
    student_login = serializers.CharField(label = "Логин")
    student_password = serializers.CharField(label = "Пароль")
    group_id = serializers.IntegerField(label = "ID Группы")
    date_of_birth = serializers.DateField(label = "Дата рождения")


class StudentRegistrationResponseSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(label = "ID Профиля")