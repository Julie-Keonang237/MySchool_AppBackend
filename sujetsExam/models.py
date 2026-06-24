from django.db import models

# Create your models here.

class Subject(models.Model):
     subjectName = models.CharField(max_length=200, unique=True, verbose_name="Subject Name")
     subjectCode = models.CharField(max_length=20, unique=False, verbose_name="Subject Code")
     description = models.TextField(blank=True, null=True, verbose_name="Description")
     department =  models.CharField(max_length=100, null=True, verbose_name="Department")
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.subjectName
     class Meta:
           ordering = ['-updated']

class ExamType(models.Model):
     exam_name = models.CharField( null=True, blank=True, max_length=100)
     SUBSYSTEM_CHOICES = (
        ("ANGLOPHONE", "Anglophone"),
        ("FRANCOPHONE", "Francophone"),
    )
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)
     subsystem = models.CharField(null=True, blank=True, max_length=20, choices=SUBSYSTEM_CHOICES,)

     

     def __str__(self):
          return self.exam_name
     class Meta:
           ordering = ['-updated']

class Paper(models.Model):
     paper_title = models.CharField(max_length=100, null=True, blank=True)
     year = models.DateField(null=True, blank=True)
     session = models.CharField(max_length=50, null = True, blank=True)
     subjectName = models.ForeignKey(Subject, on_delete= models.CASCADE)
     file = models.FileField(upload_to = 'documents/', null = True, blank=True)
     
     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)


     def __str__(self):
          return self.paper_title
     class Meta:
           ordering = ['-updated']

class ExamSubject(models.Model):
    subjectName = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_name = models.ForeignKey(ExamType, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subjectName.subjectName   # ✅ correct field access

    class Meta:
        ordering = ['-updated']