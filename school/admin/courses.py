from django.contrib import admin
from django.db.models import Avg, Count

from ..models import Course, Teacher


class TeacherNameFilter(admin.SimpleListFilter):
    title = "Teacher Name"
    parameter_name = "teacher"

    def lookups(self, request, model_admin):
        teachers = Teacher.objects.order_by("name").values_list("id", "name")
        return [(str(pk), name) for pk, name in teachers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(teacher__id=self.value())
        return queryset

class ReviewsCountFilter(admin.SimpleListFilter):
    title = "Reviews"
    parameter_name = "reviews_bucket"

    def lookups(self, request, model_admin):
        return (("5+", "At least 5 reviews"),)

    def queryset(self, request, queryset):
        value = self.value()
        if value == "5+":
            return queryset.filter(reviews_count__gte=5)
        return queryset


@admin.register(Course)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher__name", "avg_rating_display", "reviews_count")
    list_filter = (TeacherNameFilter, ReviewsCountFilter)
    search_fields = ("title", "teacher__name")
    ordering = ("title",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .with_rating_stats()
            .select_related("teacher")
        )

    def avg_rating_display(self, obj):
        return round(obj.avg_rating or 0, 2)

    avg_rating_display.short_description = "Average Rating"
    avg_rating_display.admin_order_field = "avg_rating"

    def reviews_count(self, obj):
        return obj.reviews_count

    reviews_count.admin_order_field = "reviews_count"