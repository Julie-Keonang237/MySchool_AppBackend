from django.shortcuts import render
from .models import Correction, Videos
from rest_framework.response import Response
from .serializers import CorrectionSerializer, VideoSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.views import status
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

@api_view(["GET", "POST"])
def get_CorrectionType(request):
    queryset = Correction.objects.all()
    serializer = CorrectionSerializer(queryset, many=True)
    return Response({
        "data": serializer.data,   
    })



class CorrectionAPICrud(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = CorrectionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Correction uploaded successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 


    def patch(self, request, id):

        try:
            correction = Correction.objects.get(id=id)

        except Correction.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Correction not found"
            }, status=404)

        serializer = CorrectionSerializer(
            correction,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "status": "success",
                "message": "correction updated successfully",
                "data": serializer.data
            })

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def put(self, request, id):
        try:
            paper = Correction.objects.get(id=id)
        except Correction.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

        serializer = CorrectionSerializer(paper, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Correction updated successfully",
                "data": serializer.data
            }, status=200)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def delete(self, request, id):

        try:
            correction = Correction.objects.get(id=id)

        except Correction.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Correction not found"
            }, status=404)

        correction.delete()

        return Response({
            "status": "success",
            "message": "Correction deleted successfully"
        })  

class CorrectionListAPI(APIView):
    def get(self, request):

        try:
            correction  = Correction.objects.all()

            serializer = CorrectionSerializer(correction, many=True)

            return Response({
                "status": "success",
                "data": serializer.data
            })
        
        except Correction.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Correction not found"
            }, status=404) 
         

class CorrectionperAPI(APIView):



    # def get(self, request):

    #     paper_id = request.query_params.get(
    #         'paper_id'
    #     )

    #     print("paper_id =", paper_id)

    #     queryset = Correction.objects.all()

    #     if paper_id:
    #         queryset = queryset.filter(
    #             correct_title_id=paper_id
    #         )

    #     serializer = CorrectionSerializer(
    #         queryset,
    #         many=True
    #     )

    #     print(serializer.data)

    #     return Response(serializer.data)
    
     def get(self, request, id=None):

        if id is not None:
            ...
        
        corrections = Correction.objects.all()

        paper  = request.query_params.get('paper')
        

        if paper:
            corrections = corrections.filter(
                paper_id=paper
            )

       
        serializer = CorrectionSerializer(
            corrections,
            many=True
        )
        return Response(serializer.data)
    
    

            
class CorrectionDetailAPI(APIView):
    def get(self, request, id):

        try:
            correction = Correction.objects.get(id=id)

            serializer = CorrectionSerializer(correction)

            return Response({
                "status": "success",
                "data": serializer.data
            })

        except Correction.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Correction not found"
            }, status=404)   



class CorrectionVideosAPI(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = VideoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Correction video  uploaded successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 

    #get all Corrections 


def patch(self, request, id):

    try:
        video = Videos.objects.get(id=id)

    except Videos.DoesNotExist:

        return Response({
            "status": "error",
            "message": " correction Video  not found"
        }, status=404)

    serializer = VideoSerializer(
        video,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        serializer.save()

        return Response({
            "status": "success",
            "message": "Correction Video updated successfully",
            "data": serializer.data
        })

    return Response({
        "status": "error",
        "errors": serializer.errors
    }, status=400)

def put(self, request, id):
    try:
        video = Videos.objects.get(id=id)
    except Videos.DoesNotExist:
        return Response(
            {"error": "Not found"},
            status=404
        )

    serializer = VideoSerializer(video, data=request.data)

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
        video = Videos.objects.get(id=id)

    except Videos.DoesNotExist:

        return Response({
            "status": "error",
            "message": "Correction video not found"
        }, status=404)

    video.delete()

    return Response({
        "status": "success",
        "message": "Correction Video deleted successfully"
    })
    
class VideoListAPI(APIView):
    def get(self, request):
        try:
            videos = Videos.objects.all()  # This is correct ✓
            serializer = VideoSerializer(videos, many=True)  # This is correct ✓
            return Response({
                "status": "success",
                "data": serializer.data
            })
        except Videos.DoesNotExist:  # Changed from Correction.DoesNotExist
            return Response({
                "status": "error",
                "message": "No videos found"
            }, status=404)
        
class VideoDetailAPI(APIView):
    def get(self, request, id):
        try:
            video = Videos.objects.get(id=id)  # Changed from Correction to Videos
            serializer = VideoSerializer(video)  # Changed from CorrectionSerializer
            return Response({
                "status": "success",
                "data": serializer.data
            })
        except Videos.DoesNotExist:  # Changed exception
            return Response({
                "status": "error",
                "message": "Video not found"
            }, status=404)

    
