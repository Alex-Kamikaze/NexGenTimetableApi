from django.contrib import admin
from .models import Group, Teacher, Timetable, Subject, Substitution, Exam, Examinator
# Register your models here.

class TimetableAdminModel(admin.ModelAdmin):
    search_fields = ("group_id__group_name", "day_of_week")

class ExamAdminModel(admin.ModelAdmin):
    search_fields = ("group_id__group_name", "date_of_exam")

class ExaminatorsAdminModel(admin.ModelAdmin):
    search_fields = ("teacher_id__teacher_name", "exam_id__subject_for_exam__subject_name", "exam_id__group_id__group_name")

admin.site.register(Group)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Timetable, TimetableAdminModel)
admin.site.register(Substitution)
admin.site.register(Exam, ExamAdminModel)
admin.site.register(Examinator, ExaminatorsAdminModel)