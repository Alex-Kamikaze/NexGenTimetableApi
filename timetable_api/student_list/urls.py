from django.urls import path
from .views import *

urlpatterns = [
    path("register", AddStudentView.as_view(), name="register-student")
]