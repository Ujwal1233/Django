from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('staff', 'Staff'),
)


LEAVE_TYPE_CHOICES = (
    ('casual', 'Casual Leave'),
    ('sick', 'Sick Leave'),
    ('earned', 'Earned Leave'),
)


LEAVE_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')

    def __str__(self):
        return self.user.username


class LeaveRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES, default='pending')
    admin_comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('End date must be greater than or equal to start date.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f'{self.user.username} - {self.leave_type} ({self.status})'