from rest_framework.routers import DefaultRouter
from django.urls import path
from main.views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from main.apps import MainConfig


app_name = MainConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
]

urlpatterns += router.urls