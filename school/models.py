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
            reviews_count=Count("rating"),
            avg_rating=Avg("rating__rating"),
        )

class Course(models.Model):
    objects = CourseQuerySet.as_manager()
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) 
    students = models.ManyToManyField(Student, related_name='courses')
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField()

class CourseMaterial(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    material_type = models.CharField(max_length=20)
    link = models.URLField()

class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
