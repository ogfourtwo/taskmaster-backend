from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Meeting, MeetingMinutes, Task
from .serializers import UserSerializer, MeetingSerializer, MeetingMinutesSerializer, TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class MeetingMinutesViewSet(viewsets.ModelViewSet):
    queryset = MeetingMinutes.objects.all()
    serializer_class = MeetingMinutesSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
