from django.urls import path
from subjectChapters import views
from .views import *



# Define app_name for namespacing
app_name = 'subjectChapters'


urlpatterns = [

    
    path('subject/', SubjectAPI.as_view(), name='subject'), 
    path('subject/<int:id>/', SubjectAPI.as_view(), name='subject-update-delete'),
    path("subjects/", SubjectListAPI.as_view(), name="subject-list"),
    path("subjects/<int:id>/", SubjectDetailAPI.as_view(), name="subject-detail"),

    # path('correction/<int:id>/', CorrectionAPI.as_view(), name='correction-detail'),

    path('chapter/', ChapterAPI.as_view(), name='chapter-create'),
    path('chapter/<int:id>/', ChapterAPI.as_view(), name='chapter-update-delete'),
    path('chapters/', ChapterListAPI.as_view(), name='chapter-list'),
    path('chapters/<int:id>/', ChapterDetailAPI.as_view(), name='chapter-detail'),
  
]