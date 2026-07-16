from rest_framework  import serializers
from .models import OptionModel, Level, SubjectLevel



class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionModel
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class SubjectLevelSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source='sub_name.id', read_only=True)
    subject_name = serializers.CharField(source='sub_name.subjectName', read_only=True)
    level_id = serializers.IntegerField(source='level_name.id', read_only=True)

    class Meta:
        model = SubjectLevel
        fields = ['id', 'level_id', 'subject_id', 'subject_name']
