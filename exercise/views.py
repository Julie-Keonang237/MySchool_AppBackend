from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
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
            exercise  = Exercise.objects.all()

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
 