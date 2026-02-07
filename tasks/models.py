# tasks/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_SUPERADMIN = 'superadmin'
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLE_CHOICES = [
        (ROLE_SUPERADMIN, 'SuperAdmin'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_USER, 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)
    
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': ROLE_ADMIN},
        related_name='managed_users'
    )

    def is_superadmin(self):
        return self.role == self.ROLE_SUPERADMIN

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_user(self):
        return self.role == self.ROLE_USER

class Task(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey('tasks.User', on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING)
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.assigned_to.username})"
