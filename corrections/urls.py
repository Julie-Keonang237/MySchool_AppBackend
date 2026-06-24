from django.urls import path

from .views import *
from corrections import views


# Define app_name for namespacing
app_name = 'corrections'


urlpatterns = [

    # path('correction/', get_CorrectionType, name = 'correction'),
    path('correction/', CorrectionAPI.as_view(), name='correction'),
    path('correction/<int:id>/', CorrectionAPI.as_view(), name='correction-update-delete'), 
    path("correctionl/", CorrectionListAPI.as_view(), name="correction-list"),
    path("correctionl/<int:id>/", CorrectionDetailAPI.as_view(), name="correction-detail"),

    # path('correction/<int:id>/', CorrectionAPI.as_view(), name='correction-detail'),

    path('video/', CorrectionVideosAPI.as_view(), name='video-create'),
    path('video/<int:id>/', CorrectionVideosAPI.as_view(), name='video-update-delete'),
    path('videol/', VideoListAPI.as_view(), name='video-list'),
    path('videol/<int:id>/', VideoDetailAPI.as_view(), name='video-detail'),
  
]