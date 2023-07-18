from django.db import models
from users.models import User

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


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    payment_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_choices = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=10, choices=payment_method_choices)

    def __str__(self):
        return f"{self.user.email} - {self.payment_date}"
