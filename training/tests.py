from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Course

class CourseTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.client = APIClient()
        self.client.login(username='admin', password='admin123')

    def test_create_course(self):
        data = {
            'title': 'Python',
            'description': 'Basics',
            'duration': 40
        }
        response = self.client.post('/api/courses/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 1)
