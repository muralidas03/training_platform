from django import forms
from .models import Course, TrainingSchedule, StudentTraining, Student
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class TrainingScheduleForm(forms.ModelForm):
    class Meta:
        model = TrainingSchedule
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'address']

class StudentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudentTrainingForm(forms.ModelForm):
    class Meta:
        model = StudentTraining
        fields = ['training_schedule', 'status']
