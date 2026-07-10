from django.db import models
from sujetsExam.models import Paper

# Create your models here.
class Correction(models.Model):
     correct_title = models.CharField(max_length=100)
    # subjectName= models.CharField(max_length=100)
     correct_file = models.FileField(upload_to = 'documents/', null = True, blank=True)
     paper_title  = models.ForeignKey(Paper, on_delete= models.CASCADE)
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return self.correct_title
     

class Videos(models.Model):
     title = models.CharField(max_length= 100)
     description= models.CharField(max_length=100)
     correct_title = models.ForeignKey(Correction, on_delete= models.CASCADE)
     video = models.FileField(upload_to = 'videos/')
     video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return self.title
     