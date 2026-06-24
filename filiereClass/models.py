from django.db import models

from subjectChapters.models import Subject

# Create your models here.
class OptionModel(models.Model):
     option_name = models.CharField(max_length= 100, verbose_name="option Name")
     description = models.CharField(max_length=100, verbose_name="description")
     department = models.CharField(max_length=200, blank=True, verbose_name="Department")
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return self.option_name


class Level(models.Model):
     level_name = models.CharField(max_length= 100)
     description = models.CharField(max_length=100)
     option_name = models.ForeignKey(OptionModel, on_delete= models.CASCADE)
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return self.level_name


class SubjectLevel(models.Model):
     level_name = models.ForeignKey(Level, on_delete=models.CASCADE)
     sub_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
def __str__(self):
        return self.level_name
