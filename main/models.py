from django.db import models

NULLABLE = {'blank': True, 'null': True}
# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='previews/', **NULLABLE)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='previews/', **NULLABLE)
    video_link = models.URLField(**NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'