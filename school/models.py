from django.db import models
from django.db.models import Avg, Count

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class CourseQuerySet(models.QuerySet):
    def with_rating_stats(self):
        return self.annotate(
            reviews_count=Count("ratings"),
            avg_rating=Avg("ratings__rating"),
        )

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    objects = CourseQuerySet.as_manager()
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) 
    students = models.ManyToManyField(Student, related_name='courses')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    tags = models.ManyToManyField(Tag, blank=True)

class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField()

class CourseMaterial(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    material_type = models.CharField(max_length=20)
    link = models.URLField()

class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

class CourseCompletion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_at = models.DateTimeField()

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course= models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField()

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course= models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid_at = models.DateTimeField()

class Wallet(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="wallet"
    )
    balance = models.DecimalField(max_digits=8, decimal_places=2)

class LessonProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched_percentage = models.IntegerField()