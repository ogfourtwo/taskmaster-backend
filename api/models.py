from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    name = models.CharField(max_length=100)
    type = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled')
        ],
        default='scheduled'
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ],
        default='medium'
    )
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
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    # Who is responsible
    ''' if user.is_manager:
            task.assigned_by = user
        else:
        task.assigned_by = meeting.organizer'''
    
    
    participants = models.ManyToManyField(
        User,
        related_name='tasks'
    )

    # Who assigned the task
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks_assigned'
    )

    details = models.TextField()
    minutes = models.ForeignKey(
        MeetingMinutes,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('inprogress', 'In Progress'),
            ('completed', 'Completed'),
            ('frozen', 'Frozen')
        ],
        default='pending'
    )

    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ],
        default='medium'
    )

    def __str__(self):
        return f"{self.name} (assigned by {self.assigned_by})"
