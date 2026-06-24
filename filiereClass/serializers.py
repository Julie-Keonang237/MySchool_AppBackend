from rest_framework  import serializers
from .models import OptionModel, Level



class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionModel
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
