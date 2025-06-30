from rest_framework import viewsets
from .models import Course, Student, TrainingSchedule, StudentTraining
from .serializers import CourseSerializer, StudentSerializer, TrainingScheduleSerializer, StudentTrainingSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class TrainingScheduleViewSet(viewsets.ModelViewSet):
    queryset = TrainingSchedule.objects.all()
    serializer_class = TrainingScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class StudentTrainingViewSet(viewsets.ModelViewSet):
    queryset = StudentTraining.objects.all()
    serializer_class = StudentTrainingSerializer
    permission_classes = [IsAuthenticated]
