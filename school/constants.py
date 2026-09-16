from django.db import models


class EnrollmentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    REFUNDED = "refunded", "Refunded"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"
    COMPLETED = "completed", "Completed"


class MaterialType(models.TextChoices):
    VIDEO = "video", "Video"
    PDF = "pdf", "PDF"
    QUIZ = "quiz", "Quiz"
    LINK = "link", "Link"
