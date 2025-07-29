from django.contrib import admin
from .models import Course, Lesson, Teacher, Student, Rating, CourseMaterial

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Rating)
admin.site.register(CourseMaterial)
