import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr_contributor', 'HR Contributor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Add a unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Add a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class JobRequirement(models.Model):
    department = models.CharField(max_length=100)
    function = models.CharField(max_length=100)
    rank = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.department} {self.function} ({self.rank})"

class Applicant(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    contact_information = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.email})"

class JobApplication(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job_requirement = models.ForeignKey(JobRequirement, on_delete=models.CASCADE)
    application_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=30)
    passcode = models.CharField(max_length=20)

    def __str__(self):
        return f"Application {self.application_number} by {self.applicant.name} for {self.job_requirement} with passcode {self.passcode}"
        
    class Meta:
        unique_together = ('applicant', 'job_requirement')

class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    resource_name = models.CharField(max_length=100)
    action = models.CharField(max_length=10)
    payload = models.JSONField()

    def __str__(self):
        return f"{self.timestamp} - {self.resource_name} - {self.action}"