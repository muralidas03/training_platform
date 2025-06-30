# training/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Course
from .forms import CourseForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'training/course_list.html'
    context_object_name = 'courses'

class CourseCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'training/course_form.html'
    success_url = reverse_lazy('course_list')

class CourseUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'training/course_form.html'
    success_url = reverse_lazy('course_list')

class CourseDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Course
    template_name = 'training/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')
