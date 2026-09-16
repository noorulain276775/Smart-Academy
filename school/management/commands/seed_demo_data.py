import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from school.constants import (
    EnrollmentStatus,
    MaterialType,
    PaymentStatus,
)
from school.models import (
    Answer,
    Certificate,
    Course,
    CourseMaterial,
    Enrollment,
    Lesson,
    LessonProgress,
    Payment,
    Question,
    Quiz,
    Rating,
    Student,
    Tag,
    Teacher,
    Wallet,
)

TEACHERS = [
    {
        "name": "Noor Fatima",
        "email": "noor@academy.com",
        "bio": "Senior Django engineer.",
    },
    {
        "name": "Ali Raza",
        "email": "ali@academy.com",
        "bio": "Machine learning specialist.",
    },
    {
        "name": "Sara Malik",
        "email": "sara@academy.com",
        "bio": "Cloud architect.",
    },
    {
        "name": "Hamza Khan",
        "email": "hamza@academy.com",
        "bio": "Frontend mentor.",
    },
    {
        "name": "Ayesha Siddiqui",
        "email": "ayesha@academy.com",
        "bio": "DevOps expert.",
    },
]

COURSES = [
    {"title": "Django Mastery", "teacher": "Noor Fatima", "price": "189.00"},
    {"title": "APIs with DRF", "teacher": "Noor Fatima", "price": "159.00"},
    {"title": "ML Fundamentals", "teacher": "Ali Raza", "price": "210.00"},
    {"title": "Pandas for Data Analysis", "teacher": "Ali Raza", "price": "145.00"},
    {"title": "Cloud Deployments", "teacher": "Sara Malik", "price": "175.00"},
    {"title": "Async Python", "teacher": "Sara Malik", "price": "165.00"},
    {"title": "UX Research", "teacher": "Hamza Khan", "price": "120.00"},
    {"title": "Design Systems", "teacher": "Hamza Khan", "price": "155.00"},
    {"title": "CI/CD Pipelines", "teacher": "Ayesha Siddiqui", "price": "199.00"},
    {
        "title": "Observability Deep Dive",
        "teacher": "Ayesha Siddiqui",
        "price": "185.00",
    },
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

TAGS = [
    "Python",
    "Django",
    "API",
    "Machine Learning",
    "Data Science",
    "Cloud",
    "DevOps",
    "Frontend",
    "UX",
]

COMMENTS = [
    "Excellent course.",
    "Loved the practical examples.",
    "Highly recommended.",
    "Very clear explanations.",
    "Great instructor.",
]

EMAIL_DOMAINS = [
    "smartacademy.io",
    "example.edu",
    "learners.dev",
]

QUIZZES = [
    "Module Assessment",
    "Knowledge Check",
    "Final Quiz",
]

QUESTION_TEMPLATES = [
    "What is the primary purpose of this concept?",
    "Which statement is correct?",
    "What is the best practice here?",
    "Which option would you choose?",
    "What happens when this operation runs?",
]


class Command(BaseCommand):
    help = "Generate demo data"

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)

        self._clear_data()

        self._create_teachers()
        self._create_students()
        self._create_tags()
        self._create_courses()
        self._create_enrollments()
        self._create_payments()
        self._create_wallets()
        self._create_lessons()
        self._create_quizzes()
        self._create_materials()
        self._create_materials()
        self._create_progress()
        self._create_ratings()
        self._create_certificates()

        self.stdout.write(self.style.SUCCESS("Demo data generated successfully."))

    def _clear_data(self):
        Certificate.objects.all().delete()
        Payment.objects.all().delete()
        LessonProgress.objects.all().delete()
        Rating.objects.all().delete()
        CourseMaterial.objects.all().delete()
        Lesson.objects.all().delete()
        Enrollment.objects.all().delete()
        Wallet.objects.all().delete()
        Course.objects.all().delete()
        Tag.objects.all().delete()
        Student.objects.all().delete()
        Teacher.objects.all().delete()

    def _create_teachers(self):
        Teacher.objects.bulk_create([Teacher(**teacher) for teacher in TEACHERS])

        self.teachers = {teacher.name: teacher for teacher in Teacher.objects.all()}

    def _create_students(self):
        students = []

        for index, name in enumerate(STUDENT_NAMES, start=1):
            slug = slugify(name)
            domain = random.choice(EMAIL_DOMAINS)

            students.append(
                Student(
                    name=name,
                    email=f"{slug}{index}@{domain}",
                )
            )

        Student.objects.bulk_create(students)

        self.students = list(Student.objects.all())

    def _create_tags(self):
        Tag.objects.bulk_create([Tag(name=tag) for tag in TAGS])

        self.tags = list(Tag.objects.all())

    def _create_courses(self):
        courses = []

        for blueprint in COURSES:
            courses.append(
                Course(
                    title=blueprint["title"],
                    teacher=self.teachers[blueprint["teacher"]],
                    price=Decimal(blueprint["price"]),
                    slug=slugify(blueprint["title"]),
                    description=f"Learn {blueprint['title']} from industry experts.",
                    is_published=True,
                )
            )

        Course.objects.bulk_create(courses)

        self.courses = list(Course.objects.select_related("teacher"))

        for course in self.courses:
            course.tags.set(
                random.sample(
                    self.tags,
                    random.randint(1, 3),
                )
            )

    def _create_enrollments(self):
        enrollments = []

        for course in self.courses:
            students = random.sample(
                self.students,
                random.randint(8, 18),
            )

            for student in students:
                enrollments.append(
                    Enrollment(
                        student=student,
                        course=course,
                        status=EnrollmentStatus.ACTIVE,
                    )
                )

        Enrollment.objects.bulk_create(enrollments)

        self.enrollments = list(
            Enrollment.objects.select_related(
                "student",
                "course",
            )
        )

    def _create_payments(self):
        payments = []

        for enrollment in self.enrollments:
            payments.append(
                Payment(
                    enrollment=enrollment,
                    amount=enrollment.course.price,
                    currency="EUR",
                    status=PaymentStatus.COMPLETED,
                    transaction_id=f"TXN-{random.randint(100000, 999999)}",
                    paid_at=timezone.now(),
                )
            )

        Payment.objects.bulk_create(payments)

    def _create_wallets(self):
        Wallet.objects.bulk_create(
            [
                Wallet(
                    student=student,
                    balance=Decimal(random.randint(0, 500)),
                )
                for student in self.students
            ]
        )

    def _create_lessons(self):
        lessons = []

        for course in self.courses:
            for order in range(1, 6):
                lessons.append(
                    Lesson(
                        title=f"{course.title} - Lesson {order}",
                        course=course,
                        duration_minutes=random.choice([30, 45, 60, 90]),
                        order=order,
                        is_preview=(order == 1),
                    )
                )

        Lesson.objects.bulk_create(lessons)

        self.lessons = list(Lesson.objects.select_related("course"))

    def _create_materials(self):
        materials = []

        material_types = list(MaterialType.values)

        for lesson in self.lessons:
            for _ in range(2):
                material_type = random.choice(material_types)

                materials.append(
                    CourseMaterial(
                        lesson=lesson,
                        material_type=material_type,
                        link=f"https://academy.com/materials/{slugify(lesson.title)}",
                    )
                )

        CourseMaterial.objects.bulk_create(materials)

    def _create_progress(self):
        progress_records = []

        for student in self.students:
            lessons = random.sample(
                self.lessons,
                random.randint(
                    5,
                    min(20, len(self.lessons)),
                ),
            )

            for lesson in lessons:
                progress_records.append(
                    LessonProgress(
                        student=student,
                        lesson=lesson,
                        watched_percentage=random.randint(
                            10,
                            100,
                        ),
                    )
                )

        LessonProgress.objects.bulk_create(
            progress_records,
            ignore_conflicts=True,
        )

    def _create_ratings(self):
        ratings = []

        for course in self.courses:
            enrollments = Enrollment.objects.filter(course=course)

            students = [enrollment.student for enrollment in enrollments]

            if not students:
                continue

            reviewers = random.sample(
                students,
                min(
                    len(students),
                    random.randint(2, 8),
                ),
            )

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

    def _create_certificates(self):
        completed = random.sample(
            self.enrollments,
            len(self.enrollments) // 4,
        )

        certificates = []

        for enrollment in completed:
            enrollment.status = EnrollmentStatus.COMPLETED
            enrollment.completed_at = timezone.now()
            enrollment.save()

            certificates.append(
                Certificate(
                    enrollment=enrollment,
                    issued_at=timezone.now(),
                )
            )

        Certificate.objects.bulk_create(certificates)

    def _create_quizzes(self):
        quizzes = []

        for lesson in self.lessons:
            quizzes.append(
                Quiz(
                    lesson=lesson,
                    title=random.choice(QUIZZES),
                )
            )

        Quiz.objects.bulk_create(quizzes)

        self.quizzes = list(Quiz.objects.select_related("lesson"))

        self.stdout.write(f"Created {len(self.quizzes)} quizzes")

        self._create_questions()

    def _create_questions(self):
        questions = []

        for quiz in self.quizzes:
            for _ in range(5):
                questions.append(
                    Question(
                        quiz=quiz,
                        text=random.choice(QUESTION_TEMPLATES),
                    )
                )

        Question.objects.bulk_create(questions)

        self.questions = list(Question.objects.select_related("quiz"))

        self.stdout.write(f"Created {len(self.questions)} questions")

        self._create_answers()

    def _create_answers(self):
        answers = []

        for question in self.questions:
            correct_index = random.randint(0, 3)

            for index in range(4):
                answers.append(
                    Answer(
                        question=question,
                        text=f"Option {index + 1}",
                        is_correct=index == correct_index,
                    )
                )

        Answer.objects.bulk_create(answers)

        self.stdout.write(f"Created {len(answers)} answers")
