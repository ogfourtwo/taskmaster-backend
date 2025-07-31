from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    name = models.CharField(max_length=100)
    type = models.TextField(blank=True)
    date_and_time = models.DateTimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_meetings')
    participants = models.ManyToManyField(User, related_name='meetings_attended')

    def __str__(self):
        return self.name


class MeetingMinutes(models.Model):
    summary = models.TextField(blank=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='minutes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Minutes for {self.meeting.name}"


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
        return f"Task from {self.minutes.meeting.name} - {self.details[:30]}"
