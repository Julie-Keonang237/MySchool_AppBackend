from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from corrections.models import Correction, Videos
from sujetsExam.models import Paper, Subject


class CorrectionsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='tester@example.com',
            user_name='Tester',
            user_surname='User',
            telephone='670000000',
            role='admin',
            password='pass1234',
            passwordConfirm='pass1234',
        )
        self.client.force_authenticate(user=self.user)

        self.subject = Subject.objects.create(
            subjectName='Mathematics',
            subjectCode='MATH',
        )
        self.paper = Paper.objects.create(
            paper_title='Math Paper 2025',
            subjectName=self.subject,
        )
        self.correction = Correction.objects.create(
            correct_title='Main correction',
            paper_title=self.paper,
        )

    def test_list_corrections_returns_frontend_shape(self):
        url = reverse('corrections:correction-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]['paper'], self.paper.id)
        self.assertEqual(response.data[0]['paper_title'], self.paper.paper_title)

    def test_filter_corrections_by_paper(self):
        url = reverse('corrections:correction-by-paper')
        response = self.client.get(url, {'paper': self.paper.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.correction.id)

    def test_create_video_with_url_only(self):
        url = reverse('corrections:video-create')
        payload = {
            'video_title': 'Solve exercise 1',
            'description': 'Guided correction',
            'correction': self.correction.id,
            'video_url': 'https://example.com/video/1',
        }

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['correction'], self.correction.id)
        self.assertEqual(response.data['video_title'], payload['video_title'])
        self.assertEqual(Videos.objects.count(), 1)

    def test_filter_videos_by_correction(self):
        video = Videos.objects.create(
            title='Explain chapter',
            description='Short explanation',
            correct_title=self.correction,
            video_url='https://example.com/video/2',
        )

        url = reverse('corrections:video-by-correction')
        response = self.client.get(url, {'correction_id': self.correction.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], video.id)
        self.assertEqual(response.data[0]['correct_title'], self.correction.correct_title)
