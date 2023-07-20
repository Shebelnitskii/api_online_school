from rest_framework import serializers
from .models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lessons(self, course):
        return course.lessons.count()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
