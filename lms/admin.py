from django.contrib import admin
from .models import Course, Lesson, Enrollment, UserLesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_coming_soon', 'created_at']
    list_filter = ['is_coming_soon']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'progress']
    list_filter = ['course', 'enrolled_at']

@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'completed_at']
    list_filter = ['is_completed', 'lesson__course']