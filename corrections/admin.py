from django.contrib import admin

from corrections.models import Correction, Videos
from sujetsExam.models import ExamType

# Register your models here.
admin.site.register(Correction)
admin.site.register(Videos)