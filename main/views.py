from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course, Lesson, Payment, Subscription
from .pagination import LessonPagination, CoursePagination
from .permissions import IsOwnerOnly, IsStaffNotCreateOrDelete, IsStaffUpdate, IsOwnerAndStaffList
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from main.tasks import send_update_course

# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    """ Course View Set """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListView(generics.ListAPIView):
    """ Lesson List View """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    # permission_classes = [IsAuthenticated, IsOwnerAndStaffList]
    ### Открыть для тестов
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonCreateView(generics.CreateAPIView):
    """ Lesson Create View """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsStaffNotCreateOrDelete]
    ### Открыть для тестов
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

        course_id = new_lesson.course_id
        lesson_id = new_lesson.id
        send_update_course.delay(course_id, lesson_id)




class LessonDetailView(generics.RetrieveAPIView):
    """ Lesson Detail View """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOnly]
    ### Открыть для тестов
    permission_classes = [AllowAny]


class LessonDeleteView(generics.DestroyAPIView):
    """ Lesson Delete View """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsStaffNotCreateOrDelete | IsOwnerOnly]
    ### Открыть для тестов
    permission_classes = [AllowAny]


class LessonUpdateView(generics.UpdateAPIView):
    """ Lesson Update View """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOnly | IsStaffUpdate]
    ### Открыть для тестов
    permission_classes = [AllowAny]


class PaymentListView(generics.ListAPIView):
    """ Payment List View """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson')
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class PaymentCreateView(generics.CreateAPIView):
    """ Payment Create View """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionCreateView(generics.CreateAPIView):
    """ Subscription Create View """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAuthenticated]
    ### Открыть для тестов
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionDeleteView(generics.DestroyAPIView):
    """ Subscription Delete View """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAuthenticated]
    ### Открыть для тестов
    permission_classes = [AllowAny]

    def get_object(self):
        course_id = self.kwargs['course_id']
        return Subscription.objects.get(user=self.request.user, course_id=course_id)

def payment_endpoint():
    pass