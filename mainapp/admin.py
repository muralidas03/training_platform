from django.contrib import admin
from .models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'duration']

@admin.register(TrainingSchedule)
class TrainingScheduleAdmin(admin.ModelAdmin):
    list_display = ['course', 'start_date', 'end_date', 'location']

@admin.register(StudentTraining)
class StudentTrainingAdmin(admin.ModelAdmin):
    list_display = ['student', 'training_schedule', 'status']
