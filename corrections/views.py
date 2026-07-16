import os

from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Correction, Videos
from .serializers import CorrectionSerializer, VideoSerializer


class CorrectionAPICrud(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = CorrectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            correction = Correction.objects.get(id=id)
        except Correction.DoesNotExist:
            return Response({'detail': 'Correction not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CorrectionSerializer(correction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            correction = Correction.objects.get(id=id)
        except Correction.DoesNotExist:
            return Response({'detail': 'Correction not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CorrectionSerializer(correction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            correction = Correction.objects.get(id=id)
        except Correction.DoesNotExist:
            return Response({'detail': 'Correction not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CorrectionSerializer(correction)
        payload = serializer.data
        correction.delete()
        return Response(payload, status=status.HTTP_200_OK)


class CorrectionListAPI(APIView):
    def get(self, request):
        corrections = Correction.objects.all()
        serializer = CorrectionSerializer(corrections, many=True)
        return Response(serializer.data)


class CorrectionperAPI(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                correction = Correction.objects.get(id=id)
            except Correction.DoesNotExist:
                return Response({'detail': 'Correction not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CorrectionSerializer(correction)
            return Response(serializer.data)

        corrections = Correction.objects.all()
        paper = request.query_params.get('paper')

        if paper is not None and paper != '':
            try:
                paper_id = int(str(paper).strip())
            except (TypeError, ValueError):
                return Response({'detail': 'Invalid paper query parameter'}, status=status.HTTP_400_BAD_REQUEST)

            corrections = corrections.filter(paper_title_id=paper_id)

        serializer = CorrectionSerializer(corrections, many=True)
        return Response(serializer.data)


class CorrectionDetailAPI(APIView):
    def get(self, request, id):
        try:
            correction = Correction.objects.get(id=id)
        except Correction.DoesNotExist:
            return Response({'detail': 'Correction not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CorrectionSerializer(correction)
        return Response(serializer.data)


class DownloadCorrectionView(APIView):
    def get(self, request, id):
        try:
            correction = Correction.objects.get(id=id)
        except Correction.DoesNotExist:
            raise Http404('Correction not found')

        if not correction.correct_file:
            raise Http404('No file attached to this correction')

        file_path = correction.correct_file.path
        if not os.path.exists(file_path):
            raise Http404('File not found on server')

        filename = os.path.basename(file_path)
        response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class CorrectionVideosAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            video = Videos.objects.get(id=id)
        except Videos.DoesNotExist:
            return Response({'detail': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            video = Videos.objects.get(id=id)
        except Videos.DoesNotExist:
            return Response({'detail': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            video = Videos.objects.get(id=id)
        except Videos.DoesNotExist:
            return Response({'detail': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video)
        payload = serializer.data
        video.delete()
        return Response(payload, status=status.HTTP_200_OK)


class VideoListAPI(APIView):
    def get(self, request):
        videos = Videos.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


class VideoByCorrectionAPI(APIView):
    def get(self, request):
        videos = Videos.objects.all()
        correction_id = request.query_params.get('correction_id')

        if correction_id is not None and correction_id != '':
            try:
                correction_id = int(str(correction_id).strip())
            except (TypeError, ValueError):
                return Response({'detail': 'Invalid correction_id query parameter'}, status=status.HTTP_400_BAD_REQUEST)

            videos = videos.filter(correct_title_id=correction_id)

        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


class VideoDetailAPI(APIView):
    def get(self, request, id):
        try:
            video = Videos.objects.get(id=id)
        except Videos.DoesNotExist:
            return Response({'detail': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video)
        return Response(serializer.data)
