from django.core.management.base import BaseCommand
from django.utils import timezone
from lms.models import Course, Lesson

class Command(BaseCommand):
    help = 'Populate initial courses and lessons'

    def handle(self, *args, **options):
        # WordPress Course
        wp_course, created = Course.objects.get_or_create(
            title='WordPress Masterclass',
            description='10-Day Crash Masterclass to Master WordPress.',
            is_coming_soon=False
        )
        if created:
            days = [
                ('Day 1: Install and Set Up WordPress', 'Download WordPress... (full content from previous)'),
                # Add all 10 days' content here - truncated for brevity
                ('Day 2: Plan Your Site Structure', 'Brainstorm your site...'),
                # ... up to Day 10
                ('Day 10: Launch, Maintain, and Next Steps', 'Backup everything...'),
            ]
            for i, (title, content) in enumerate(days, 1):
                Lesson.objects.create(course=wp_course, title=title, content=content, order=i)
            self.stdout.write(self.style.SUCCESS('WordPress course populated'))

        # Coming Soon
        Course.objects.get_or_create(title='Python Programming', description='Coming Soon: Python Crash Course.', is_coming_soon=True)
        Course.objects.get_or_create(title='Artificial Intelligence', description='Coming Soon: AI Fundamentals.', is_coming_soon=True)

        self.stdout.write(self.style.SUCCESS('Coming soon courses added'))