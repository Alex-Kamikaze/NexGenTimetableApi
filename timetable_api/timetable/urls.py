from django.urls import path
from .views import *

urlpatterns = [
    path("groups/all", GroupListView.as_view(), name="get-all-groups"),
    path("teachers/all", TeacherView.as_view(), name="get-all-teachers"),
    path("timetable/for-group/<int:group_id>", TimetableForGroupView.as_view(), name="get-timetable-for-group")
]