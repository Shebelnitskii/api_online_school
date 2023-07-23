from rest_framework import serializers
from .models import Course, Lesson, Payment, Subscription
import re


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    def validate(self, data):
        data = super().validate(data)

        # Проверяем ссылку на видео
        video_link = data.get('video_link')
        if video_link and not re.match(r'^https?://(?:www\.)?youtube\.com/', video_link):
            raise serializers.ValidationError("Недопустимая ссылка на видео.")

        return data
class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lessons(self, course):
        count = int(course.lesson_set.count())
        return count

    def validate(self, data):
        data = super().validate(data)

        # Проверяем ссылку на видео
        video_link = data.get('video_link')
        if video_link and not re.match(r'^https?://(?:www\.)?youtube\.com/', video_link):
            raise serializers.ValidationError("Недопустимая ссылка на видео.")

        return data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

