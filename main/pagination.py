from rest_framework.pagination import PageNumberPagination


class LessonPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'lesson_page_size'
    max_page_size = 5


class CoursePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'course_page_size'
    max_page_size = 3
