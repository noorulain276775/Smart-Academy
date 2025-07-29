from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Course(models.Model):
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
