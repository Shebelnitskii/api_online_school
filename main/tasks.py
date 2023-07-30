from django.utils import timezone
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from main.models import Course, Subscription, Lesson
from users.models import User


@shared_task
def send_update_course(course_id, lesson_id):
    try:
        course = Course.objects.get(pk=course_id)
        lesson = course.lesson_set.get(pk=lesson_id)
        subscribers = Subscription.objects.filter(course=course).select_related('user')

        subject = f'Новый урок в курсе "{course.name}"'
        body = f'Тема урока "{lesson.name}" от пользователя: {lesson.owner}'
        from_email = settings.EMAIL_HOST_USER

        # Отправка писем всем подписчикам
        for subscription in subscribers:
            to_email = subscription.user.email
            send_mail(subject, body, from_email, [to_email])

    except:
        print('Ошибка отправки письма')


@shared_task
def check_inactive_users():
    # Получаем текущую дату и вычитаем 30 дней для определения пороговой даты
    last_login_date = timezone.now() - timedelta(days=30)

    # Получаем пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(last_login__lt=last_login_date, is_active=True)

    # Блокируем пользователей установкой флага is_active в False
    inactive_users.update(is_active=False)