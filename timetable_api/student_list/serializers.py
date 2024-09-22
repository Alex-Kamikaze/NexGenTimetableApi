from rest_framework import serializers

class StudentRegistrationResponseSerializer(serializer.Serializer):
    student_id = serializers.IntegerField(label = "ID Профиля")