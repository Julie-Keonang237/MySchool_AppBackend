from django.contrib import admin

from sujetsExam.models import ExamSubject, ExamType, Paper, Subject

# Register your models here.
admin.site.register(ExamType)
admin.site.register(Paper)
admin.site.register(Subject)
admin.site.register(ExamSubject)
