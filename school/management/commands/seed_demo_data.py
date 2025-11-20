import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from school.models import (
    Course,
    CourseMaterial,
    Lesson,
    Rating,
    Student,
    Teacher,
)

TEACHERS = [
    {"name": "Noor Fatima", "bio": "Senior Django engineer who loves API performance."},
    {"name": "Ali Raza", "bio": "Data scientist focused on practical machine learning."},
    {"name": "Sara Malik", "bio": "Cloud architect helping teams ship scalable backends."},
    {"name": "Hamza Khan", "bio": "Frontend mentor with a passion for delightful UX."},
    {"name": "Ayesha Siddiqui", "bio": "DevOps advocate and automation champion."},
]

COURSES = [
    {"title": "Django Mastery", "teacher": "Noor Fatima", "price": "189.00"},
    {"title": "APIs with DRF", "teacher": "Noor Fatima", "price": "159.00"},
    {"title": "ML Fundamentals", "teacher": "Ali Raza", "price": "210.00"},
    {"title": "Pandas for Data Analysis", "teacher": "Ali Raza", "price": "145.00"},
    {"title": "Cloud Deployments", "teacher": "Sara Malik", "price": "175.00"},
    {"title": "Async Python", "teacher": "Sara Malik", "price": "165.00"},
    {"title": "UX Research 101", "teacher": "Hamza Khan", "price": "120.00"},
    {"title": "Design Systems", "teacher": "Hamza Khan", "price": "155.00"},
    {"title": "CI/CD Pipelines", "teacher": "Ayesha Siddiqui", "price": "199.00"},
    {"title": "Observability Deep Dive", "teacher": "Ayesha Siddiqui", "price": "185.00"},
]

STUDENT_NAMES = [
    "Alina Qureshi",
    "Bilal Ahmed",
    "Cyrus Iqbal",
    "Dania Farooq",
    "Eman Tariq",
    "Faraz Imran",
    "Ghazal Javed",
    "Hassan Rafi",
    "Imaan Yousaf",
    "Jibran Saleem",
    "Khalid Hussain",
    "Laiba Faisal",
    "Mahnoor Saeed",
    "Nabeel Shah",
    "Omar Siddique",
    "Parisa Khan",
    "Qasim Rehman",
    "Rania Noor",
    "Saad Ilyas",
    "Tania Aslam",
    "Usman Khalid",
    "Vania Javed",
    "Waleed Anwar",
    "Xenia Rehman",
    "Yasir Shah",
    "Zara Chaudhry",
]

MATERIAL_TYPES = ["video", "article", "quiz", "notebook", "assignment"]
COMMENTS = [
    "Loved the pacing and the real-world examples.",
    "Great instructor energy!",
    "I finally understand this topic.",
    "Challenging but rewarding assignments.",
    "Helpful office hours and community.",
]
EMAIL_DOMAINS = ["smartacademy.io", "example.edu", "learners.dev"]


class Command(BaseCommand):
    help = "Populate the database with a rich demo dataset for manual testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--append",
            action="store_true",
            help="Add demo data without clearing existing records.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)
        append = options["append"]

        if not append:
            self.stdout.write(self.style.WARNING("Clearing previous demo data..."))
            self._clear_data()

        self._create_teachers()
        self._create_students()
        self._create_courses()
        self._attach_students_to_courses()
        self._create_lessons_and_materials()
        self._create_ratings()

        self.stdout.write(self.style.SUCCESS("Demo data successfully generated!"))
        self._print_summary()

    def _clear_data(self):
        CourseMaterial.objects.all().delete()
        Lesson.objects.all().delete()
        Rating.objects.all().delete()
        Course.objects.all().delete()
        Student.objects.all().delete()
        Teacher.objects.all().delete()

    def _create_teachers(self):
        Teacher.objects.bulk_create([Teacher(**data) for data in TEACHERS])
        self.teachers = {t.name: t for t in Teacher.objects.all()}
        self.stdout.write(f"Created {len(self.teachers)} teachers")

    def _create_students(self):
        students = []
        for idx, name in enumerate(STUDENT_NAMES, start=1):
            slug = slugify(name)
            domain = random.choice(EMAIL_DOMAINS)
            students.append(
                Student(
                    name=name,
                    email=f"{slug or 'student'}{idx}@{domain}",
                )
            )
        Student.objects.bulk_create(students, ignore_conflicts=True)
        self.students = list(Student.objects.all())
        self.stdout.write(f"Created {len(self.students)} students")

    def _create_courses(self):
        courses = []
        for blueprint in COURSES:
            teacher = self.teachers[blueprint["teacher"]]
            courses.append(
                Course(
                    title=blueprint["title"],
                    teacher=teacher,
                    price=Decimal(blueprint["price"]),
                )
            )
        Course.objects.bulk_create(courses)
        self.courses = list(Course.objects.select_related("teacher"))
        self.stdout.write(f"Created {len(self.courses)} courses")

    def _attach_students_to_courses(self):
        for course in self.courses:
            cohort_size = random.randint(8, min(18, len(self.students)))
            enrolled = random.sample(self.students, cohort_size)
            course.students.set(enrolled)
        self.stdout.write("Assigned students to courses")

    def _create_lessons_and_materials(self):
        lessons = []
        for course in self.courses:
            for idx in range(1, 5):
                lessons.append(
                    Lesson(
                        title=f"{course.title} – Lesson {idx}",
                        course=course,
                        duration_minutes=random.choice([30, 45, 60, 75, 90]),
                    )
                )
        Lesson.objects.bulk_create(lessons)
        lessons = list(Lesson.objects.select_related("course"))

        materials = []
        for lesson in lessons:
            for material_type in random.sample(MATERIAL_TYPES, 2):
                materials.append(
                    CourseMaterial(
                        lesson=lesson,
                        material_type=material_type,
                        link=f"https://content.smartacademy.io/{slugify(lesson.title)}/{material_type}",
                    )
                )
        CourseMaterial.objects.bulk_create(materials)
        self.stdout.write(
            f"Created {len(lessons)} lessons and {len(materials)} course materials"
        )

    def _create_ratings(self):
        ratings = []
        for course in self.courses:
            enrolled_students = list(course.students.all())
            if not enrolled_students:
                continue
            max_reviewers = min(10, len(enrolled_students))
            reviewer_count = random.randint(2, max_reviewers)
            reviewers = random.sample(enrolled_students, reviewer_count)
            for student in reviewers:
                ratings.append(
                    Rating(
                        course=course,
                        student=student,
                        rating=random.randint(3, 5),
                        comment=random.choice(COMMENTS),
                    )
                )
        Rating.objects.bulk_create(ratings)
        self.stdout.write(f"Created {len(ratings)} ratings")

    def _print_summary(self):
        self.stdout.write("\nSummary:")
        self.stdout.write(f"  Teachers: {Teacher.objects.count()}")
        self.stdout.write(f"  Students: {Student.objects.count()}")
        self.stdout.write(f"  Courses: {Course.objects.count()}")
        self.stdout.write(f"  Lessons: {Lesson.objects.count()}")
        self.stdout.write(f"  Materials: {CourseMaterial.objects.count()}")
        self.stdout.write(f"  Ratings: {Rating.objects.count()}")
