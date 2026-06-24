# api/urls.py
from django.urls import path

from sujetsExam.views import ExamTypeAPI, get_ExamType
from .views import *


app_name = 'api'

urlpatterns = [

    # path('get_ExamType/', get_ExamType, name ='get_ExamType'),
    # path('examType/', ExamTypeAPI.as_view(), name ='examType')
    # Your API endpoints
    # path('courses/', CourseListView.as_view(), name='courses'),
    # path('students/', StudentListView.as_view(), name='students'),
    # etc.
]