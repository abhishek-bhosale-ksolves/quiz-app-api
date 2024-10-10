from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    ROLE_CHOICES = [
        ('Instructor', 'Instructor'),
        ('Student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Student')
