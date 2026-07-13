from rest_framework  import serializers
from .models import ExamSubject, ExamType, GeneratedExam, GeneratedExamItem, Paper, Subject
from django.utils import timezone
from exercise.models import Exercise
from exercise.serializers import ExerciseSerializer




class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta: 
         model = ExamType
         fields = '__all__'


class PaperSerializer(serializers.ModelSerializer):

    # Writable: accepts the Subject's PK on create/update. Was previously
    # IntegerField(read_only=True) sourced off 'subjectName.id', which meant
    # nothing ever populated the model's subjectName FK on create — every
    # upload failed with "NOT NULL constraint failed: subjectName_id".
    subject = serializers.PrimaryKeyRelatedField(
        source='subjectName',
        queryset=Subject.objects.all(),
    )

    subjectName = serializers.CharField(
        source='subjectName.subjectName',
        read_only=True
    )

    # Papers don't carry their own exam type — a paper's subject can be
    # linked to one or more exam types via ExamSubject, so this surfaces
    # those names for display purposes (e.g. "Title - Subject - ExamType"
    # pickers) without requiring a schema change.
    exam_types = serializers.SerializerMethodField()

    def get_exam_types(self, obj):
        return list(
            ExamSubject.objects.filter(subjectName=obj.subjectName)
            .values_list('exam_name__exam_name', flat=True)
            .distinct()
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
            'exam_types',
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


class GeneratedExamItemSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        source='exercise', queryset=Exercise.objects.all(), write_only=True,
    )

    class Meta:
        model = GeneratedExamItem
        fields = ['id', 'exercise', 'exercise_id', 'marks', 'order']


class GeneratedExamSerializer(serializers.ModelSerializer):
    items = GeneratedExamItemSerializer(many=True, read_only=True)
    subject_name = serializers.CharField(source='subject.subjectName', read_only=True)
    level_name = serializers.CharField(source='level.level_name', read_only=True)
    total_marks = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = GeneratedExam
        fields = [
            'id', 'title', 'subject', 'subject_name', 'level', 'level_name',
            'instructions', 'created_at', 'items', 'total_marks', 'pdf_url',
        ]

    def get_total_marks(self, obj):
        return sum(item.marks for item in obj.items.all())

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if not obj.pdf_file or not request:
            return None
        return request.build_absolute_uri(obj.pdf_file.url)