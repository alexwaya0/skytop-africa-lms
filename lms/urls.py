from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('complete-lesson/<int:lesson_id>/', views.complete_lesson, name='complete_lesson'),
]