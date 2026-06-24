from django.db import models
from sujetsExam.models import Subject

# Create your models here.



class Chapter(models.Model):
     chap_name = models.CharField(max_length= 100)
     chapter_number = models.PositiveIntegerField(verbose_name="Chapter Number")
     description = models.CharField(max_length=100)
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)

def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class SubjectChapter(models.Model):
      sub_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
      chap_name = models.ForeignKey(Chapter, on_delete=models.CASCADE)
      updated_at = models.DateTimeField(auto_now=True)
      created_at = models.DateTimeField(auto_now_add=True)
      def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
