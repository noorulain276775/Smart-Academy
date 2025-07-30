from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from django.db.models import Avg, Count
from .models import Course, Teacher, Student, Rating


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


"""
Write a Django view that returns a list of all teachers along with:
    The total number of courses they teach
    The total number of students across all their courses (count each student only once per teacher, even if enrolled in multiple courses)
Order the results by the number of students taught (descending).
The response should include:
    Teacher name
    Number of courses taught
    Number of unique students taught

"""

def teacher_course_student_stats(request):
    all_teacher_courses = Teacher.objects.annotate(course_count = Count('course', distinct=True), student_count = Count('course__students', distinct=True)).order_by('-student_count')
    result = []
    for teacher in all_teacher_courses:
        result.append({
            'Teacher name': teacher.name,
            "Number of courses": teacher.course_count,
            "Number of Unique Student taught": teacher.student_count
        })
    return JsonResponse(result, safe=False)


"""
For each teacher, return their top 3 students based on the number of courses they have taken with that specific teacher. Return a JSON list where each item looks like:
For example:

{
  "Teacher name": "John Doe",
  "Top Students": [
    {
      "Student name": "Alice",
      "Courses with teacher": 4
    },
    {
      "Student name": "Bob",
      "Courses with teacher": 3
    },
    {
      "Student name": "Charlie",
      "Courses with teacher": 2
    }
  ]
}
"""
def teachers_with_top_students(request):
    result = []
    for teacher in Teacher.objects.all():
        teacher_courses = Course.objects.filter(teacher=teacher)
        student_courses_count = Student.objects.filter(courses__in = teacher_courses).annotate(courses_with_teacher = Count('courses')).order_by('-courses_with_teacher')[:3]
        top_students = [
                    {
                        "Student name": student.name,
                        "Courses with teacher": student.courses_with_teacher
                    }
                    for student in student_courses_count
                ]
        result.append({
            "Teacher name": teacher.name,
            "Top Students": top_students

        })
    return JsonResponse(result, safe=False)



"""
Create an API view that returns a list of all courses along with:

    Course title
    Course teacher name
    Average student rating (from a related Rating model)
    Total number of enrolled students
Output Should be liked:
[
  {
    "Course Title": "Python Basics",
    "Teacher": "Mr. Ahmed",
    "Average Rating": 4.5,
    "Total Enrolled Students": 12
  },
  {
    "Course Title": "Django Advanced",
    "Teacher": "Ms. Noor",
    "Average Rating": 4.9,
    "Total Enrolled Students": 18
  }
]

"""

def course_stats(request):
    stats = Course.objects.select_related('teacher').annotate(avg_rating = Avg('rating__rating'), student_count = Count('students', distinct=True))
    result = []
    for stat in stats:
        result.append({
            "Course Title": stat.title,
            'Teacher': stat.teacher.name,
            "Average Rating": stat.avg_rating or 0,
            "Total Enrolled Students": stat.student_count
        })

    return JsonResponse(result, safe=False)

"""
Latest Rating Per Course by Any Student
Goal: Return a list of courses, each with:
  Course title
  Teacher name
  The most recent rating value (if any)

Example:
[
  {
    "Course Title": "Python Basics",
    "Teacher": "Ali Raza",
    "Latest Rating": 4.0
  },
  {
    "Course Title": "Django Mastery",
    "Teacher": "Noor",
    "Latest Rating": 5.0
  }
]

"""

def course_latest_summary(request):
    result = []
    latest_rating = Rating.objects.filter(course=OuterRef('pk')).order_by('-id') 
    courses = Course.objects.select_related('teacher').annotate(latest_rating = Subquery(latest_rating.values('rating')[:1]))
    for course in courses:
        result.append({
            "Course Title": course.title,
            "Teacher": course.teacher.name,
            "Latest Rating": course.latest_rating
        })
    return JsonResponse(result, safe=False)


"""
Average Rating per Teacher Across All Their Courses
For each teacher, return:
  Teacher name
  Total number of courses they've taught
  Average rating (based on all ratings across all their courses)

Example Output:

[
  {
    "Teacher": "Noor",
    "Total Courses": 3,
    "Average Rating": 4.67
  },
  {
    "Teacher": "Ali Raza",
    "Total Courses": 2,
    "Average Rating": 4.25
  }
]
"""

def average_rating_per_teacher(request):
    result = []
    teacher_ratings= Teacher.objects.annotate(total_course = Count('course'), average_rating= Avg('course__rating__rating'))
    for teacher in teacher_ratings:
        result.append({
            "Teacher": teacher.name,
            "Total Course": teacher.total_course,
            "Average Rating": round(teacher.average_rating or 0, 2)

        })

    return JsonResponse(result, safe=False)