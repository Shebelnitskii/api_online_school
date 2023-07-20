from rest_framework.routers import DefaultRouter
from django.urls import path
from main.views import CourseViewSet, LessonListView, LessonCreateView, LessonDetailView, LessonDeleteView, \
    LessonUpdateView, PaymentListView, PaymentCreateView
from main.apps import MainConfig

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/detail/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson-delete'),
    path('lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson-update'),
    path('payments/list/', PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
]

urlpatterns += router.urls
