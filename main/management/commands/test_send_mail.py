from django.core.management import BaseCommand
from django.core.mail import send_mail

from config import settings
from main.models import Course, Subscription


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            course = Course.objects.get(pk=2)
            lesson = course.lesson_set.get(pk=76)
            subscribers = Subscription.objects.filter(course=course).select_related('user')

            subject = f'Новый урок в курсе "{course.name}"'
            body = f'Новый урок в курсе "{course.name}"\nТема урока "{lesson.name}" от пользователя: {lesson.owner}'
            from_email = settings.EMAIL_HOST_USER

            # Отправка писем всем подписчикам
            for subscription in subscribers:
                to_email = subscription.user.email
                send_mail(subject, body, from_email, [to_email])

        except:
            print('Ошибка отправки письма')
