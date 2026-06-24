from rest_framework  import serializers
from .models import Correction, Videos



class CorrectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Correction
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'
