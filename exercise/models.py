from django.db import models

from subjectChapters.models import Subject, Chapter

# Create your models here.
class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Medium'),
        (4, 'Hard'),
        (5, 'Very Hard'),
    ]

    title = models.CharField(max_length=100, verbose_name="Title")
    content = models.CharField(max_length=500)
    marks = models.CharField(max_length=50)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, help_text="1=Very Easy, 5=Very Hard")
    sub_name = models.ForeignKey(Subject, on_delete= models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name='exercises')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    marks = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text
