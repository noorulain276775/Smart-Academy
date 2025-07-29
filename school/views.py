from django.http import JsonResponse
from django.db.models import Avg, Count
from .models import Course, Lesson, Teacher, Student, Rating, CourseMaterial


"""
Write a Django view that returns a list of all courses along with their average rating.
Only include courses that have at least 2 reviews and the average rating is greater than 3.5.
The response should include the course title and its average rating.

"""

def top_courses_with_average_rating(request):
    top_courses = Course.objects.annotate(reviews_count = Count('rating') ,avg_rating = Avg('rating__rating')).filter(reviews_count__gte= 2, avg_rating__gt=3.5)
    result = []
    for course in top_courses:
        result.append({
            'title': course.title,
            'average_rating': round(course.avg_rating, 2)
        })
    return JsonResponse(result, safe=False)
