from django.core.management import BaseCommand
from django.core.mail import send_mail

from config import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mail(
            'message_item.letter_subject',  # Тема письма
            'message_item.letter_body',  # Тело письма
            settings.EMAIL_HOST_USER,  # От кого отправляем письмо
            ['shebelnitskiy@gmail.com'],  # Кому отправляем письмо
            fail_silently=False,
        )
