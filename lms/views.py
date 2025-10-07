from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Course, Lesson, Enrollment, UserLesson

def home(request):
    courses = Course.objects.filter(is_coming_soon=False)
    coming_soon = Course.objects.filter(is_coming_soon=True)
    featured_course = courses.first()  # Assume first course is featured (WordPress)
    return render(request, 'lms/home.html', {
        'courses': courses,
        'coming_soon': coming_soon,
        'featured_course': featured_course
    })

def courses(request):
    all_courses = Course.objects.all()
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(user=request.user)
        enrolled_courses = {en.course.id: en for en in enrollments}
    else:
        enrolled_courses = {}
    return render(request, 'lms/courses.html', {'courses': all_courses, 'enrolled_courses': enrolled_courses})

def about(request):
    return render(request, 'lms/about.html')

def contact(request):
    return render(request, 'lms/contact.html')

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'lms/dashboard.html', {'enrollments': enrollments})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_authenticated:
        enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
        user_lessons = UserLesson.objects.filter(user=request.user, lesson__course=course)
        completed_ids = {ul.lesson.id for ul in user_lessons if ul.is_completed}
        enrollment.progress = enrollment.progress_percentage
        enrollment.save()
    else:
        enrollment = None
        completed_ids = set()
    lessons = course.lessons.all()
    return render(request, 'lms/course_detail.html', {
        'course': course,
        'enrollment': enrollment,
        'lessons': lessons,
        'completed_ids': completed_ids
    })

@require_POST
@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = Enrollment.objects.get(user=request.user, course=lesson.course)
    user_lesson, created = UserLesson.objects.get_or_create(user=request.user, lesson=lesson)
    if not user_lesson.is_completed:
        user_lesson.is_completed = True
        user_lesson.completed_at = timezone.now()
        user_lesson.save()
        enrollment.progress = enrollment.progress_percentage
        enrollment.save()
    return JsonResponse({'success': True, 'progress': enrollment.progress_percentage})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'lms/login.html', {'form': form})