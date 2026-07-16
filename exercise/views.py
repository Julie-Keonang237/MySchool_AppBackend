from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import random
from .models import Exercise
from rest_framework.response import Response
from .serializers import ExerciseSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.views import status

# Create your views here.

# @api_view(["GET", "POST"])
# def get_CorrectionType(request):
#     queryset = OptionModel.objects.all()
#     serializer = OptionSerializer(queryset, many=True)
#     return Response({
#         "data": serializer.data,   
#     })



class ExerciseAPI(APIView):

    def post(self, request):

        serializer = ExerciseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Exercises added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 


    
    def put(self, request, id):
        try:
            exercise = Exercise.objects.get(id=id)
        except Exercise.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

        serializer = ExerciseSerializer(exercise, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Exercises updated successfully",
                "data": serializer.data
            }, status=200)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def delete(self, request, id):

        try:
            exercise = Exercise.objects.get(id=id)

        except Exercise.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Exercise not found"
            }, status=404)

        exercise.delete()

        return Response({
            "status": "success",
            "message": "Exercises deleted successfully"
        }) 



class ExerciseListAPI(APIView):
    def get(self, request):

        try:
            exercise = Exercise.objects.all()

            subject = request.query_params.get('subject')
            if subject:
                exercise = exercise.filter(sub_name_id=subject)

            chapter = request.query_params.get('chapter')
            if chapter:
                exercise = exercise.filter(chapter_id=chapter)

            min_difficulty = request.query_params.get('min_difficulty')
            if min_difficulty:
                exercise = exercise.filter(difficulty__gte=min_difficulty)

            max_difficulty = request.query_params.get('max_difficulty')
            if max_difficulty:
                exercise = exercise.filter(difficulty__lte=max_difficulty)

            serializer = ExerciseSerializer(exercise, many=True)

            return Response({
                "status": "success",
                "data": serializer.data
            })

        except Exercise.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Exercises not found"
            }, status=404)


class DrawExercisesAPI(APIView):
    """
    Draws a random sample of exercises per chapter for exam generation.
    Expects: [{"chapter_id": int, "count": int, "min_difficulty": int|null, "max_difficulty": int|null}, ...]
    Returns exercises grouped under each selection, capped to however many
    are actually available (no error if a chapter has fewer exercises than
    requested — the draw is just as large as it can be).
    """

    def post(self, request):
        selections = request.data
        if not isinstance(selections, list):
            return Response({
                "status": "error",
                "message": "Expected a list of chapter selections"
            }, status=status.HTTP_400_BAD_REQUEST)

        results = []
        for selection in selections:
            chapter_id = selection.get('chapter_id')
            count = selection.get('count')
            if not chapter_id or not count:
                return Response({
                    "status": "error",
                    "message": "Each selection needs chapter_id and count"
                }, status=status.HTTP_400_BAD_REQUEST)

            pool = Exercise.objects.filter(chapter_id=chapter_id)

            min_difficulty = selection.get('min_difficulty')
            if min_difficulty:
                pool = pool.filter(difficulty__gte=min_difficulty)

            max_difficulty = selection.get('max_difficulty')
            if max_difficulty:
                pool = pool.filter(difficulty__lte=max_difficulty)

            pool = list(pool)
            drawn = random.sample(pool, min(count, len(pool)))

            results.append({
                "chapter_id": chapter_id,
                "exercises": ExerciseSerializer(drawn, many=True).data
            })

        return Response({
            "status": "success",
            "data": results
        })


class ExerciseDetailAPI(APIView):
    def get(self, request, id):

        try:
            exercise = Exercise.objects.get(id=id)

            serializer = ExerciseSerializer(exercise)

            return Response({
                "status": "success",
                "data": serializer.data
            })

        except Exercise.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Exercise not found"
            }, status=404)   
 