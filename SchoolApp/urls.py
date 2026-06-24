# SchoolApp/SchoolApp/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include authentication app URLs
    # All auth URLs will start with /api/auth/
    path('api/auth/', include('authentication.urls')),
    
    # Include api app URLs  
    # All API URLs will start with /api/v1/
    path('api/v1/', include('api.urls')),

    path('api/sujets/', include('sujetsExam.urls')),

    path('api/corrections/', include('corrections.urls')),

    path('api/filiereClass/', include('filiereClass.urls')),

    path('api/subjectChapters/', include('subjectChapters.urls')),

     path('api/exercise/', include('exercise.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )