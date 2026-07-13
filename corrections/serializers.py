from rest_framework import serializers

from sujetsExam.models import Paper

from .models import Correction, Videos


class CorrectionSerializer(serializers.ModelSerializer):
    paper = serializers.PrimaryKeyRelatedField(
        source='paper_title',
        queryset=Paper.objects.all(),
    )
    paper_title = serializers.CharField(
        source='paper_title.paper_title',
        read_only=True,
    )

    class Meta:
        model = Correction
        fields = [
            'id',
            'correct_title',
            'correct_file',
            'paper',
            'paper_title',
        ]


class VideoSerializer(serializers.ModelSerializer):
    correction = serializers.PrimaryKeyRelatedField(
        source='correct_title',
        queryset=Correction.objects.all(),
    )
    video_title = serializers.CharField(source='title')
    correct_title = serializers.CharField(
        source='correct_title.correct_title',
        read_only=True,
    )

    class Meta:
        model = Videos
        fields = [
            'id',
            'video_title',
            'correction',
            'correct_title',
            'description',
            'video',
            'video_url',
        ]
