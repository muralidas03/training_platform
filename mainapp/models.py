from django.db import models
from user_management.models import User


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="%(class)s_user")
	phone = models.CharField(max_length=20,)
	address = models.TextField()
	def __str__(self):
		return f'{self.user}'

class Course(models.Model):
	title = models.CharField(max_length=255,)
	description = models.TextField()
	duration = models.PositiveIntegerField()
	def __str__(self):
		return f'{self.title}'

class TrainingSchedule(models.Model):
	course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='%(class)s_course')
	start_date = models.DateField()
	end_date = models.DateField()
	location = models.CharField(max_length=255,)
	def __str__(self):
		return f'{self.pk}'

class StudentTraining(models.Model):
	student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='%(class)s_student')
	training_schedule = models.ForeignKey('TrainingSchedule', on_delete=models.CASCADE, related_name='%(class)s_training_schedule')
	status = models.CharField(max_length=10,choices=[('opt_in', 'Opt_in'), ('opt_out', 'Opt_out')],)
	def __str__(self):
		return f'{self.pk}'
