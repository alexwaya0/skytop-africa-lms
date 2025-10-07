from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_coming_soon = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def total_lessons(self):
        return self.lesson_set.count()

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)  # Auto-updated via signal or view

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    @property
    def completed_lessons(self):
        return self.user.userlesson_set.filter(lesson__course=self.course).count()

    @property
    def progress_percentage(self):
        if self.course.total_lessons == 0:
            return 0
        return int((self.completed_lessons / self.course.total_lessons) * 100)

class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f"{self.user.username} completed {self.lesson.title}"