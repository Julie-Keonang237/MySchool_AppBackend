from django.urls import path

from .views import *
from sujetsExam import views


# Define app_name for namespacing
app_name = 'sujetsExam'


urlpatterns = [

    #path('get_ExamType/', get_ExamType, name = 'get_ExamType'),
    path('examType/', ExamTypeAPI.as_view(), name = 'examType'),
    path('examTypes/', ExamTypeAPIcrud.as_view(), name = 'examType-create-update-delete-list'),

    #path('get_Paper/', get_Paper, name='get_Paper'),
    path('papercrud/', PaperAPIcrud.as_view(), name='paper'),
    path('paper/', PaperAPI.as_view(), name='paper'),
    path('paperone/<int:id>/', PaperDetailsAPI.as_view(), name='paper-detail'),
    path('papers/', PaperListAPI.as_view(), name='paper-List'),
    path('paperdownload/<int:id>/', DownloadPaperView.as_view(), name='paper-download'),

    path('subjectcrud/', SubjetAPIcrud.as_view(), name='subject'),
    path('subjectsE/', SubjectPerTypeAPI.as_view(), name='subject-per-ExamType'),

   
]