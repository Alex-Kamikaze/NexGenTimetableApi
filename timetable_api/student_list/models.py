from django.db import models
from timetable.models import Group

# Create your models here.
class Student(models.Model):
    fio = models.TextField(verbose_name = "ФИО Студента")
    date_of_birth = models.DateField(verbose_name = "Дата рождения")
    group_id = models.ForeignKey(Group, on_delete = models.CASCADE)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.fio
