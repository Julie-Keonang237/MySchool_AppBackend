from rest_framework  import serializers
from .models import Correction, Videos





class CorrectionSerializer(serializers.ModelSerializer):

    paper = serializers.IntegerField(
        source='paper_title.id',
        read_only=True
    )

    paper_title = serializers.CharField(
        source='paper_title.paper_title',
        read_only=True
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
    class Meta:
        model = Videos
        fields = '__all__'
