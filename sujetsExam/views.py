from django.shortcuts import render
from django.core.files.base import ContentFile
from .models import ExamType
from .models import Paper
from .models import Subject
from .models import ExamSubject
from .models import GeneratedExam, GeneratedExamItem
from rest_framework.response import Response
from .serializers import ExamSubjectSerializer, ExamTypeSerializer
from .serializers import SubjectSerializer
from .serializers import GeneratedExamSerializer
from .pdf import render_exam_pdf
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
        
    def put(self, request, id):                     # id from the path
        try:
            exam_type = ExamType.objects.get(id=id)  # use the path id
        except ExamType.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Exam type not found"
            }, status=404)

        serializer = ExamTypeSerializer(exam_type, data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "errors": serializer.errors,
            }, status=400)

        serializer.save()
        return Response({
            "status": "success",
            "message": "Exam type updated successfully",
            "data": serializer.data
        }, status=200)

    def patch(self, request, id):                  # id from the path
        try:
            exam_type = ExamType.objects.get(id=id)
        except ExamType.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Exam type not found"
            }, status=404)

        serializer = ExamTypeSerializer(exam_type, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "errors": serializer.errors,
            }, status=400)

        serializer.save()
        return Response({
            "status": "success",
            "message": "Exam type updated successfully",
            "data": serializer.data
        }, status=200)

    def delete(self, request, id):                 # id from the path
        try:
            exam_type = ExamType.objects.get(id=id)
        except ExamType.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Exam type not found"
            }, status=404)

        exam_type.delete()
        return Response({
            "status": "success",
            "message": "Exam type deleted successfully"
        }, status=200)
        
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
        
    def put(self, request, id):                     # id comes from the path
        try:
            subject = Subject.objects.get(id=id)    # use the path id
        except Subject.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Subject not found"
            }, status=404)

        serializer = SubjectSerializer(subject, data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "errors": serializer.errors,
            }, status=400)

        serializer.save()
        return Response({
            "status": "success",
            "message": "Subject updated successfully",
            "data": serializer.data
        }, status=200)

    def patch(self, request, id):                  # id comes from the path
        try:
            subject = Subject.objects.get(id=id)    # use the path id
        except Subject.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Subject not found"
            }, status=404)

        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "errors": serializer.errors,
            }, status=400)

        serializer.save()
        return Response({
            "status": "success",
            "message": "Subject updated successfully",
            "data": serializer.data
        }, status=200)

    def delete(self, request, id):                 # id comes from the path
        try:
            subject = Subject.objects.get(id=id)    # use the path id
        except Subject.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Subject not found"
            }, status=404)

        subject.delete()
        return Response({
            "status": "success",
            "message": "Subject deleted successfully"
        }, status=200)
        
        
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
                subjectName_id=subject
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


class GeneratedExamListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exams = GeneratedExam.objects.filter(created_by=request.user)
        serializer = GeneratedExamSerializer(exams, many=True, context={'request': request})
        return Response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        data = request.data
        items_data = data.get('items', [])

        if not items_data:
            return Response({
                "status": "error",
                "message": "At least one exercise item is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam = GeneratedExam.objects.create(
                title=data.get('title', ''),
                subject_id=data.get('subject_id'),
                level_id=data.get('level_id'),
                instructions=data.get('instructions', ''),
                created_by=request.user,
            )
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        for order, item in enumerate(items_data):
            GeneratedExamItem.objects.create(
                exam=exam,
                exercise_id=item['exercise_id'],
                marks=item['marks'],
                order=item.get('order', order),
            )

        pdf_buffer = render_exam_pdf(exam)
        exam.pdf_file.save(f"exam_{exam.id}.pdf", ContentFile(pdf_buffer.read()), save=True)

        serializer = GeneratedExamSerializer(exam, context={'request': request})
        return Response({
            "status": "success",
            "message": "Exam generated successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class GeneratedExamDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            exam = GeneratedExam.objects.get(id=id, created_by=request.user)
        except GeneratedExam.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Generated exam not found"
            }, status=404)

        serializer = GeneratedExamSerializer(exam, context={'request': request})
        return Response({
            "status": "success",
            "data": serializer.data
        })


class DownloadGeneratedExamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            exam = GeneratedExam.objects.get(id=id, created_by=request.user)
        except GeneratedExam.DoesNotExist:
            raise Http404("Generated exam not found")

        if not exam.pdf_file:
            raise Http404("No PDF attached to this exam")

        file_path = exam.pdf_file.path
        if not os.path.exists(file_path):
            raise Http404("File not found on server")

        filename = os.path.basename(file_path)
        response = FileResponse(
            open(file_path, "rb"),
            content_type="application/pdf"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response