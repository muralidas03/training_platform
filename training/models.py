from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class TrainingSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course.title} - {self.start_date}"

class StudentTraining(models.Model):
    STATUS_CHOICES = (('opt_in', 'Opt In'), ('opt_out', 'Opt Out'))
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    training_schedule = models.ForeignKey(TrainingSchedule, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'training_schedule')

    def __str__(self):
        return f"{self.student} - {self.training_schedule} ({self.status})"
