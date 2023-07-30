from django.urls import reverse
from rest_framework import serializers

import config.settings
from .models import Course, Lesson, Payment, Subscription
import re
import stripe

stripe.api_key = config.settings.STRIPE_API_KEY


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
    is_subscribed = serializers.SerializerMethodField()
    url_payments = serializers.SerializerMethodField()
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

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscription_set.filter(user=request.user).exists()
        return False

    def get_url_payments(self, course):
        payment = stripe.Product.create(name=course.name, )
        price = stripe.Price.create(
            unit_amount=int(course.price)*100,
            currency="usd",
            product=payment['id'],
        )
        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price": price['id'],
                    "quantity": 1,
                },
            ],
            mode="payment",
        )

        return session['url']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
