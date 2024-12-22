from django.contrib import admin
from .models import Group, Teacher, Timetable, Subject, Substitution
# Register your models here.

class TimetableAdminModel(admin.ModelAdmin):
    search_fields = ("group_id__group_name", "day_of_week")

admin.site.register(Group)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Timetable, TimetableAdminModel)
admin.site.register(Substitution)