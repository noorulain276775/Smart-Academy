from django.urls import path
from .views import top_courses_with_average_rating, teacher_course_student_stats, teachers_with_top_students

urlpatterns = [
    path('top-courses/', top_courses_with_average_rating),
    path('teacher-courses/', teacher_course_student_stats),
    path('teacher-students/', teachers_with_top_students)
]