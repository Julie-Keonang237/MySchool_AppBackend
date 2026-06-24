from django.shortcuts import render
from .models import ExamType
from .models import Paper
from .models import Subject
from .models import ExamSubject
from rest_framework.response import Response
from .serializers import ExamSubjectSerializer, ExamTypeSerializer
from .serializers import SubjectSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.views import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import PaperSerializer
from rest_framework.permissions import IsAuthenticated
import os
from django.http import Http404, FileResponse, HttpResponse




@api_view(["GET", "POST"])
def get_ExamType(request):
    queryset = ExamType.objects.all()
    serializer = ExamTypeSerializer(queryset, many=True)
    return Response({
        "data": serializer.data,   
    })



class ExamTypeAPIcrud(APIView):

    def get(self, request):

        exam_types = ExamType.objects.all()

        serializer = ExamTypeSerializer(
            exam_types,
            many=True
        )

        return Response({
            "status": "success",
            "data": serializer.data
        })
    
    def post(self, request):
        data = request.data
        serializer = ExamTypeSerializer(data=data)
        if not serializer.is_valid():     
            return Response({
                "Message": "data not saved",
                "errors": serializer.errors,
            })
        serializer.save()
        return Response({
            "Message": "data saved correctly",
            "data": serializer.data
        })
        
    def put(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "Message": "data not updated",
                "errors": "id is required",
            })
        
        try:
            examType = ExamType.objects.get(id=data.get('id'))
        except ExamType.DoesNotExist:
            return Response({
                "Message": "data not updated",
                "errors": "Exam type not found"
            }, status=404)
        
        serializer = ExamTypeSerializer(examType, data=data)
        if not serializer.is_valid():     
            return Response({
                "Message": "data not updated correctly",
                "errors": serializer.errors,
            })
        serializer.save()
        return Response({
            "Message": "data updated correctly",
            "data": serializer.data
        })
    
    def patch(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "Message": "data not updated",
                "errors": "id is required",
            })
        
        try:
            examType = ExamType.objects.get(id=data.get('id'))
        except ExamType.DoesNotExist:
            return Response({
                "Message": "data not updated",
                "errors": "Exam type not found"
            }, status=404)
        
        serializer = ExamTypeSerializer(examType, data=data, partial=True)
        if not serializer.is_valid():     
            return Response({
                "Message": "data not saved",
                "errors": serializer.errors,
            })
        serializer.save()
        return Response({
            "Message": "data saved correctly",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "message": "Data not deleted",
                "errors": "id is required"
            }, status=400)
        
        try:
            exam_type = ExamType.objects.get(id=data.get('id'))
            exam_type.delete()
            return Response({
                "message": "Data deleted successfully"
            }, status=200)
        except ExamType.DoesNotExist:
            return Response({
                "message": "Data not deleted",
                "errors": "Exam type not found"
            }, status=404)
        
class ExamTypeAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        subsystem = request.query_params.get('subsystem')

        print("SUBSYSTEM =", subsystem)

        queryset = ExamType.objects.all()

        if subsystem:
            queryset = queryset.filter(
                subsystem=subsystem
            )

        serializer = ExamTypeSerializer(
            queryset,
            many=True
        )

        return Response(serializer.data)
    
class SubjetAPIcrud(APIView):

    def get(self, request):

        subjects = Subject.objects.all()

        serializer = SubjectSerializer(
            subjects,
            many=True
        )

        return Response({
            "status": "success",
            "data": serializer.data
        })
    
    def post(self, request):
        data = request.data
        serializer = SubjectSerializer(data=data)
        if not serializer.is_valid():     
            return Response({
                "Message": "data not saved",
                "errors": serializer.errors,
            })
        serializer.save()
        return Response({
            "Message": "data saved correctly",
            "data": serializer.data
        })
        
    def put(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "Message": "data not updated",
                "errors": "id is required",
            })
        
        try:
            subjects = Subject.objects.get(id=data.get('id'))
        except Subject.DoesNotExist:
            return Response({
                "Message": "data not updated",
                "errors": "Exam type not found"
            }, status=404)
        
        serializer = SubjectSerializer(subjects, data=data)
        if not serializer.is_valid():     
            return Response({
                "Message": "data not updated correctly",
                "errors": serializer.errors,
            })
        serializer.save()
        return Response({
            "Message": "data updated correctly",
            "data": serializer.data
        })
    
    def patch(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "Message": "data not updated",
                "errors": "id is required",
            })
        
        try:
            subjects = Subject.objects.get(id=data.get('id'))
        except Subject.DoesNotExist:
            return Response({
                "Message": "data not updated",
                "errors": "Subject not found"
            }, status=404)
        
        serializer = SubjectSerializer(subjects, data=data, partial=True)
        if not serializer.is_valid():     
            return Response({
                "Message": "data not saved",
                "errors": serializer.errors,
            })
        serializer.save()
        return Response({
            "Message": "data saved correctly",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "message": "Data not deleted",
                "errors": "id is required"
            }, status=400)
        
        try:
            subjects = Subject.objects.get(id=data.get('id'))
            subjects.delete()
            return Response({
                "message": "Data deleted successfully"
            }, status=200)
        except Subject.DoesNotExist:
            return Response({
                "message": "Data not deleted",
                "errors": "Exam type not found"
            }, status=404)
        
        
class SubjectPerTypeAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        exam_type_id = request.query_params.get(
            'exam_type_id'
        )

        print("exam_type_id =", exam_type_id)

        queryset = ExamSubject.objects.all()

        if exam_type_id:
            queryset = queryset.filter(
                exam_name_id=exam_type_id
            )

        serializer = ExamSubjectSerializer(
            queryset,
            many=True
        )

        print(serializer.data)

        return Response(serializer.data)
    # #get all papers
    # class AllSubjectsAPI(APIView):


    #     papers = Paper.objects.all()

    #     serializer = PaperSerializer(papers, many=True)

    #     return Response({
    #         "status": "success",
    #         "data": serializer.data
    #     })

        
class PaperAPIcrud(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = PaperSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Paper uploaded successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 

    
   
    def patch(self, request, id):

        try:
            paper = Paper.objects.get(id=id)

        except Paper.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Paper not found"
            }, status=404)

        serializer = PaperSerializer(
            paper,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "status": "success",
                "message": "Paper updated successfully",
                "data": serializer.data
            })

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def put(self, request, id):
        try:
            paper = Paper.objects.get(id=id)
        except Paper.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

        serializer = PaperSerializer(paper, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Paper updated successfully",
                "data": serializer.data
            }, status=200)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def delete(self, request, id):

        try:
            paper = Paper.objects.get(id=id)

        except Paper.DoesNotExist:

            return Response({
                "status": "error",
                "message": "Paper not found"
            }, status=404)

        paper.delete()

        return Response({
            "status": "success",
            "message": "Paper deleted successfully"
        })

class PaperAPI(APIView):

    def get(self, request, id=None):

        if id is not None:
            ...
        
        papers = Paper.objects.all()

        subject  = request.query_params.get('subjectName')
        year = request.query_params.get('year')
        session = request.query_params.get('session')

        if subject:
            papers = papers.filter(
                subject_id=subject
            )

        if year:
            papers = papers.filter(
                year__year=year
            )

        if session:
            papers = papers.filter(
                session=session
            )

        serializer = PaperSerializer(
            papers,
            many=True
        )

        return Response(serializer.data)
        
class PaperListAPI(APIView):
    #get all papers 

    def get(self, request):

        papers = Paper.objects.all()

        serializer = PaperSerializer(papers, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        })

class PaperDetailsAPI(APIView):
        #get one paper
   def get(self, request, id):

    print("Paper requested:", id)

    try:
        paper = Paper.objects.get(id=id)

        serializer = PaperSerializer(paper)

        print(serializer.data)

        return Response({
            "status": "success",
            "data": serializer.data
        })

    except Paper.DoesNotExist:

        print("Paper not found")

        return Response({
            "status": "error",
            "message": "Paper not found"
        }, status=404)

class DownloadPaperView(APIView):

    def get(self, request, id):

        try:
            paper = Paper.objects.get(id=id)

        except Paper.DoesNotExist:
            raise Http404("Paper not found")

        if not paper.file:
            raise Http404("No file attached to this paper")

        file_path = paper.file.path

        if not os.path.exists(file_path):
            raise Http404("File not found on server")

        filename = os.path.basename(file_path)

        response = FileResponse(
            open(file_path, "rb"),
            content_type="application/pdf"
        )
        # print('Status code: ${response.response.statusCode}'):
        # print('Content-type: ${response.response.headers.value('content-type')}'):
        # print('Bytes length: ${response.data.length}'):
        response["Content-Disposition"] = (
            f'attachment; filename="{filename}"'
        )

        return response