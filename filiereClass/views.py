from django.shortcuts import render
from .models import OptionModel, Level
from rest_framework.response import Response
from .serializers import OptionSerializer, LevelSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.views import status

# Create your views here.

@api_view(["GET", "POST"])
def get_CorrectionType(request):
    queryset = OptionModel.objects.all()
    serializer = OptionSerializer(queryset, many=True)
    return Response({
        "data": serializer.data,   
    })



class OptionAPI(APIView):

    def post(self, request):

        serializer = OptionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Options added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 


    
    def put(self, request, id):
        try:
            option = OptionModel.objects.get(id=id)
        except OptionModel.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

        serializer = OptionSerializer(option, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Options updated successfully",
                "data": serializer.data
            }, status=200)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def delete(self, request, id):

        try:
            option = OptionModel.objects.get(id=id)

        except OptionModel.DoesNotExist:

            return Response({
                "status": "error",
                "message": "option not found"
            }, status=404)

        option.delete()

        return Response({
            "status": "success",
            "message": "Option deleted successfully"
        }) 



class OptionListAPI(APIView):
    def get(self, request):

        try:
            option  = OptionModel.objects.all()

            serializer = OptionSerializer(option, many=True)

            return Response({
                "status": "success",
                "data": serializer.data
            })
        
        except OptionModel.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Option not found"
            }, status=404)   
 
        
class OptionDetailAPI(APIView):
    def get(self, request, id):

        try:
            option = OptionModel.objects.get(id=id)

            serializer = OptionSerializer(option)

            return Response({
                "status": "success",
                "data": serializer.data
            })

        except OptionModel.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Option not found"
            }, status=404)   
 


class LevelAPI(APIView):

    def post(self, request):

        serializer = LevelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": " Level added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 

    #get all Corrections 

    def put(self, request, id):
        try:
            level  = Level.objects.get(id=id)
        except Level.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

        serializer = LevelSerializer(level, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Correction video updated successfully",
                "data": serializer.data
            }, status=200)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def delete(self, request, id):

        try:
            level = Level.objects.get(id=id)

        except Level.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Correction video not found"
            }, status=404)

        level.delete()

        return Response({
            "status": "success",
            "message": "Correction Video deleted successfully"
        })
    
class LevelListAPI(APIView):
    def get(self, request):
        try:
            level = Level.objects.all()  # This is correct ✓
            serializer = LevelSerializer(level, many=True)  # This is correct ✓
            return Response({
                "status": "success",
                "data": serializer.data
            })
        except Level.DoesNotExist:  # Changed from Correction.DoesNotExist
            return Response({
                "status": "error",
                "message": "No levels found"
            }, status=404)
        
class LevelDetailAPI(APIView):
    def get(self, request, id):
        try:
            level = Level.objects.get(id=id)  # Changed from Correction to Videos
            serializer = LevelSerializer(level)  # Changed from CorrectionSerializer
            return Response({
                "status": "success",
                "data": serializer.data
            })
        except Level.DoesNotExist:  # Changed exception
            return Response({
                "status": "error",
                "message": "Level not found"
            }, status=404)

    
