from django.urls import path
from filiereClass import views
from .views import *



# Define app_name for namespacing
app_name = 'filiereClass'


urlpatterns = [

    
    path('option/', OptionAPI.as_view(), name='option'), 
    path('option/<int:id>/', OptionAPI.as_view(), name='option-update-delete'),
    path("options/", OptionListAPI.as_view(), name="option-list"),
    path("options/<int:id>/", OptionDetailAPI.as_view(), name="option-detail"),

    # path('correction/<int:id>/', CorrectionAPI.as_view(), name='correction-detail'),

    path('level/', LevelAPI.as_view(), name='level-create'),
    path('level/<int:id>/', LevelAPI.as_view(), name='level-update-delete'),
    path('levels/', LevelListAPI.as_view(), name='level-list'),
    path('levels/<int:id>/', LevelDetailAPI.as_view(), name='level-detail'),
    path('subjects-for-level/', SubjectsForLevelAPI.as_view(), name='subjects-for-level'),

]