from rest_framework  import serializers
from .models import Exercise, Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'text', 'marks', 'order']


class ExerciseSerializer(serializers.ModelSerializer):
    # Nested and writable: DRF's ModelSerializer doesn't support nested
    # writes out of the box, so create/update below replace the exercise's
    # question set wholesale from whatever list is posted.
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Exercise
        fields = [
            'id', 'title', 'content', 'marks', 'difficulty',
            'sub_name', 'chapter', 'questions', 'updated', 'created',
        ]

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        exercise = Exercise.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(exercise=exercise, **question_data)
        return exercise

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if questions_data is not None:
            instance.questions.all().delete()
            for question_data in questions_data:
                Question.objects.create(exercise=instance, **question_data)

        return instance
