from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from django.db.models import Avg, Count, F, Window
from .models import Course, Teacher, Student, Rating
from django.db.models.functions import RowNumber


"""
Write a Django view that returns a list of all courses along with their average rating.
Only include courses that have at least 2 reviews and the average rating is greater than 3.5.
The response should include the course title and its average rating.

"""


def top_courses_with_average_rating(request):
    top_courses = Course.objects.annotate(
        reviews_count=Count("rating"), avg_rating=Avg("rating__rating")
    ).filter(reviews_count__gte=2, avg_rating__gt=3.5)
    result = []
    for course in top_courses:
        result.append(
            {"title": course.title, "average_rating": round(course.avg_rating, 2)}
        )
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
    all_teacher_courses = Teacher.objects.annotate(
        course_count=Count("course", distinct=True),
        student_count=Count("course__students", distinct=True),
    ).order_by("-student_count")
    result = []
    for teacher in all_teacher_courses:
        result.append(
            {
                "Teacher name": teacher.name,
                "Number of courses": teacher.course_count,
                "Number of Unique Student taught": teacher.student_count,
            }
        )
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
        student_courses_count = (
            Student.objects.filter(courses__in=teacher_courses)
            .annotate(courses_with_teacher=Count("courses"))
            .order_by("-courses_with_teacher")[:3]
        )
        top_students = [
            {
                "Student name": student.name,
                "Courses with teacher": student.courses_with_teacher,
            }
            for student in student_courses_count
        ]
        result.append({"Teacher name": teacher.name, "Top Students": top_students})
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
    stats = Course.objects.select_related("teacher").annotate(
        avg_rating=Avg("rating__rating"), student_count=Count("students", distinct=True)
    )
    result = []
    for stat in stats:
        result.append(
            {
                "Course Title": stat.title,
                "Teacher": stat.teacher.name,
                "Average Rating": stat.avg_rating or 0,
                "Total Enrolled Students": stat.student_count,
            }
        )

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
    latest_rating = Rating.objects.filter(course=OuterRef("pk")).order_by("-id")
    courses = Course.objects.select_related("teacher").annotate(
        latest_rating=Subquery(latest_rating.values("rating")[:1])
    )
    for course in courses:
        result.append(
            {
                "Course Title": course.title,
                "Teacher": course.teacher.name,
                "Latest Rating": course.latest_rating,
            }
        )
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
    teacher_ratings = Teacher.objects.annotate(
        total_course=Count("course"), average_rating=Avg("course__rating__rating")
    )
    for teacher in teacher_ratings:
        result.append(
            {
                "Teacher": teacher.name,
                "Total Course": teacher.total_course,
                "Average Rating": round(teacher.average_rating or 0, 2),
            }
        )

    return JsonResponse(result, safe=False)


"""
For each teacher, find their top 2 courses ranked by the number of unique students enrolled.
Return JSON with teacher name and top 2 course titles with student counts.

Imagine this output of queryset so that we can make our JSON according to that

<QuerySet [{'teacher_id': 1, 'teacher__name': 'Alice Johnson', 'title': 'Django Mastery', 'student_count': 10, 'row_number': 1}, 
{'teacher_id': 1, 'teacher__name': 'Alice Johnson', 'title': 'APIs with DRF', 'student_count': 8, 'row_number': 2}, 
{'teacher_id': 2, 'teacher__name': 'Bob Smith', 'title': 'ML Fundamentals', 'student_count': 11, 'row_number': 1}, 
{'teacher_id': 2, 'teacher__name': 'Bob Smith', 'title': 'Pandas for Data Analysis', 'student_count': 9, 'row_number': 2}, 
{'teacher_id': 3, 'teacher__name': 'Carol Lee', 'title': 'UI/UX Essentials', 'student_count': 6, 'row_number': 1}, 
{'teacher_id': 3, 'teacher__name': 'Carol Lee', 'title': 'React from Zero', 'student_count': 4, 'row_number': 2}]>

"""


def topTwoCoursesOfEachTeacher(request):
    result = []
    top_courses = (
        Course.objects.annotate(student_count=Count("students", distinct=True))
        .annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F("teacher_id")],
                order_by=[F("student_count").desc(), F("id").asc()],
            )
        )
        .filter(row_number__lte=2)
        .select_related("teacher")
        .values("teacher_id", "teacher__name", "title", "student_count", "row_number")
        .order_by("teacher_id", "row_number")
    )
    print(top_courses)

    result = []
    current_teacher = None
    group = None

    for row in top_courses:
        if (
            row["teacher_id"] != current_teacher
        ):  # id -1 , current teacher is None, 2nd loop: # Id-1 and current teacher = 1
            if group:  # group is None , so in 2nd loop it does not run at all
                result.append(group)
            current_teacher = row["teacher_id"]  # New teacher recorded
            group = {
                "teacher": row["teacher__name"],
                "top_courses": [],
            }  # New group created

        group["top_courses"].append(
            {
                "title": row["title"],
                "student_count": row["student_count"],
            }
        )  # course is appended, only course appended in 2nd loop

    if group:
        result.append(group)

    return JsonResponse(result, safe=False)


"""
For each course, find the latest rating (based on id) and the student name who gave that rating.

"""


def latestRatingwithStudentName(request):
    latest_rating = Rating.objects.filter(course=OuterRef("pk")).order_by("-id")
    qs = Course.objects.annotate(
        latest_rating=Subquery(latest_rating.values("rating")[:1]),
        latest_student=Subquery(latest_rating.values("student__name")[:1]),
    ).values("id", "title", "latest_rating", "latest_student")
    return JsonResponse(list(qs), safe=False)
