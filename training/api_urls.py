from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'courses', api_views.CourseViewSet)
router.register(r'students', api_views.StudentViewSet)
router.register(r'schedules', api_views.TrainingScheduleViewSet)
router.register(r'student-trainings', api_views.StudentTrainingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
