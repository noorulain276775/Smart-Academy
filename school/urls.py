from django.urls import path
from .views import top_courses_with_average_rating, teacher_course_student_stats, teachers_with_top_students, course_stats, course_latest_summary, average_rating_per_teacher

urlpatterns = [
    path('top-courses/', top_courses_with_average_rating),
    path('teacher-courses/', teacher_course_student_stats),
    path('teacher-students/', teachers_with_top_students),
    path('course-stats/', course_stats),
    path('course-latest/', course_latest_summary),
    path('teacher-rating/', average_rating_per_teacher)
]