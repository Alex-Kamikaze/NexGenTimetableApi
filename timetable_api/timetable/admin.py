from django.contrib import admin
from .models import Group, Teacher, Timetable, Subject, Substitution
# Register your models here.
admin.site.register(Group)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Timetable)
admin.site.register(Substitution)