from rest_framework  import serializers
from .models import ExamSubject, ExamType, Paper, Subject
from django.utils import timezone




class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta: 
         model = ExamType
         fields = '__all__'


class PaperSerializer(serializers.ModelSerializer):

    subject = serializers.IntegerField(
        source='subjectName.id',
        read_only=True
    )

    subjectName = serializers.CharField(
        source='subjectName.subjectName',
        read_only=True
    )

    class Meta:
        model = Paper
        fields = [
            'id',
            'paper_title',
            'year',
            'session',
            'subject',
            'subjectName',
            'file',
        ]

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'



class ExamSubjectSerializer(serializers.ModelSerializer):

    subject = serializers.IntegerField(
        source='subjectName.id',
        read_only=True
    )

    examType = serializers.IntegerField(
        source='exam_name.id',
        read_only=True
    )

    subject_name = serializers.CharField(
        source='subjectName.subjectName',
        read_only=True
    )

    exam_name = serializers.CharField(
        source='exam_name.exam_name',
        read_only=True
    )

    class Meta:
        model = ExamSubject
        fields = [
            'id',
            'subject',
            'examType',
            'subject_name',
            'exam_name',
        ]