from django.shortcuts import render
from .models import Subject, Chapter
from rest_framework.response import Response
from  .serializers import SubjectSerializer, ChapterSerializer
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


class SubjectAPI(APIView):

    def post(self, request):

        serializer = SubjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Subject added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 


    
    def put(self, request, id):
        try:
            subject = Subject.objects.get(id=id)
        except Subject.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

        serializer = SubjectSerializer(subject, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Subjects  updated successfully",
                "data": serializer.data
            }, status=200)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def delete(self, request, id):

        try:
            option = Subject.objects.get(id=id)

        except Subject.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Subject not found"
            }, status=404)

        option.delete()

        return Response({
            "status": "success",
            "message": "Subject deleted successfully"
        }) 



class SubjectListAPI(APIView):
    def get(self, request):

        try:
            option  = Subject.objects.all()

            serializer = SubjectSerializer(option, many=True)

            return Response({
                "status": "success",
                "data": serializer.data
            })
        
        except Subject.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Subject  not found"
            }, status=404)   
 
        
class SubjectDetailAPI(APIView):
    def get(self, request, id):

        try:
            option = Subject.objects.get(id=id)

            serializer = SubjectSerializer(option)

            return Response({
                "status": "success",
                "data": serializer.data
            })

        except Subject.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Subject not found"
            }, status=404)   
 


class ChapterAPI(APIView):

    def post(self, request):

        serializer = ChapterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": " Chapters  added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 

    #get all Corrections 

    def put(self, request, id):
        try:
            chapter  = Chapter.objects.get(id=id)
        except Chapter.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

        serializer = ChapterSerializer(chapter, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Chapter updated successfully",
                "data": serializer.data
            }, status=200)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def delete(self, request, id):

        try:
            chapter = Chapter.objects.get(id=id)

        except Chapter.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Chapter not found"
            }, status=404)

        chapter.delete()

        return Response({
            "status": "success",
            "message": "Chapter deleted successfully"
        })
    
class ChapterListAPI(APIView):
    def get(self, request):
        try:
            chapter = Chapter.objects.all() 
            serializer = ChapterSerializer(chapter, many=True)  
            return Response({
                "status": "success",
                "data": serializer.data
            })
        except chapter.DoesNotExist:  
            return Response({
                "status": "error",
                "message": "No chapters found"
            }, status=404)
        
class ChapterDetailAPI(APIView):
    def get(self, request, id):
        try:
            chapter = Chapter.objects.get(id=id) 
            serializer = ChapterSerializer(chapter) 
            return Response({
                "status": "success",
                "data": serializer.data
            })
        except Chapter.DoesNotExist:  
            return Response({
                "status": "error",
                "message": "chapter not found"
            }, status=404)

    
