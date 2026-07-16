from django.urls import path
from exercise import views
from .views import *



# Define app_name for namespacing
app_name = 'exercise'


urlpatterns = [
 
    path('exercisec/', ExerciseAPI.as_view(), name='exercisec'), 
    path('exercisec/<int:id>/', ExerciseAPI.as_view(), name='exercise-update-delete'),
    path("exercises/", ExerciseListAPI.as_view(), name="exercise-list"),
    path("exercises/<int:id>/", ExerciseDetailAPI.as_view(), name="exercise-detail"),
    path("draw/", DrawExercisesAPI.as_view(), name="exercise-draw"),

   
]