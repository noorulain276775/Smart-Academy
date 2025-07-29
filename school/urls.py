from django.urls import path
from .views import top_courses_with_average_rating

urlpatterns = [
    path('top-courses', top_courses_with_average_rating)
]