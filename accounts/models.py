from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    national_code = models.DecimalField(max_digits=10, decimal_places=0, unique=True, null=True, blank=True)
    school_name = models.CharField(max_length=30, blank=True, null=True)
    lesson_name = models.CharField(max_length=30, blank=True, null=True)
