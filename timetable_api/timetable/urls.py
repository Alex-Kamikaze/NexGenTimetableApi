from django.urls import path
from .views import *

urlpatterns = [
    path("groups/all", get_group_list),
    path("teachers/all", get_all_teachers),
    path("timetable/for-group/<int:group_id>", get_timetable_for_group)
]