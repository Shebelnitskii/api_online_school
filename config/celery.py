import os
from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()


# Celery Beat Configuration
app.conf.beat_schedule = {
    'check_inactive_users': {
        'task': 'main.tasks.check_inactive_users',
        'schedule': crontab(minute=0, hour=0),  # Запускать каждый день в полночь
    },
}