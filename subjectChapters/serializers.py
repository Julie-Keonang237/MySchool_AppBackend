from rest_framework  import serializers
from .models import Subject, Chapter, SubjectChapter



class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class SubjectChapterSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source='sub_name.id', read_only=True)
    chapter = ChapterSerializer(source='chap_name', read_only=True)

    class Meta:
        model = SubjectChapter
        fields = ['id', 'subject_id', 'chapter']
