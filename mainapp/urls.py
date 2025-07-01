from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.user_login, name='user_login'),

    path('student/', views.student_list, name='student_list'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/new/', views.student_create, name='student_create'),
    path('student/<int:pk>/edit/', views.student_update, name='student_update'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('course/', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/new/', views.course_create, name='course_create'),
    path('course/<int:pk>/edit/', views.course_update, name='course_update'),
    path('course/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('trainingschedule/', views.trainingschedule_list, name='trainingschedule_list'),
    path('trainingschedule/<int:pk>/', views.trainingschedule_detail, name='trainingschedule_detail'),
    path('trainingschedule/new/', views.trainingschedule_create, name='trainingschedule_create'),
    path('trainingschedule/<int:pk>/edit/', views.trainingschedule_update, name='trainingschedule_update'),
    path('trainingschedule/<int:pk>/delete/', views.trainingschedule_delete, name='trainingschedule_delete'),
    path('studenttraining/', views.studenttraining_list, name='studenttraining_list'),
    path('studenttraining/<int:pk>/', views.studenttraining_detail, name='studenttraining_detail'),
    path('studenttraining/new/', views.studenttraining_create, name='studenttraining_create'),
    path('studenttraining/<int:pk>/edit/', views.studenttraining_update, name='studenttraining_update'),
    path('studenttraining/<int:pk>/delete/', views.studenttraining_delete, name='studenttraining_delete'),
]