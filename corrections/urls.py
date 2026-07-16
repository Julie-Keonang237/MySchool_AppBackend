from django.urls import path

from .views import *


# Define app_name for namespacing
app_name = 'corrections'


urlpatterns = [

    # path('correction/', get_CorrectionType, name = 'correction'),
    path('correction/', CorrectionAPICrud.as_view(), name='correction'),
    path('correction/<int:id>/', CorrectionAPICrud.as_view(), name='correction-update-delete'), 
    path("correctionl/", CorrectionListAPI.as_view(), name="correction-list"),
    path("correctionone/<int:id>/", CorrectionDetailAPI.as_view(), name="correction-detail"),
    path("correctionby/", CorrectionperAPI.as_view(), name="correction-by-paper"),
    path("paperdownload/<int:id>/", DownloadCorrectionView.as_view(), name="correction-download"),

    # path('correction/<int:id>/', CorrectionAPI.as_view(), name='correction-detail'),

    path('video/', CorrectionVideosAPI.as_view(), name='video-create'),
    path('video/<int:id>/', CorrectionVideosAPI.as_view(), name='video-update-delete'),
    path('videol/', VideoListAPI.as_view(), name='video-list'),
    path('videosby/', VideoByCorrectionAPI.as_view(), name='video-by-correction'),
    path('videosone/<int:id>/', VideoDetailAPI.as_view(), name='video-detail'),
  
]