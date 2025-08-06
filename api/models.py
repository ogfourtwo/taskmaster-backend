from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    title = models.CharField(max_length=100)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.title


class MeetingMinutes(models.Model):
    summary = models.TextField(blank=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='minutes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Minutes for {self.meeting.title}"


class Task(models.Model):
    deadline = models.DateTimeField()
    members = models.ManyToManyField(User, related_name='tasks')
    details = models.TextField()
    minutes = models.ForeignKey(MeetingMinutes, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('done', 'Done')],
        default='pending'
    )
    priority = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )

    def __str__(self):
        return f"Task from {self.minutes.meeting.title} - {self.details[:30]}"

class MeetingRole(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('participant', 'Participant'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'meeting')