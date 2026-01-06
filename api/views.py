from rest_framework import viewsets
from django.contrib.auth.models import User
from django.db import models
from .models import Meeting, MeetingMinutes, Task
from .serializers import UserSerializer, MeetingSerializer, MeetingMinutesSerializer, TaskSerializer
from rest_framework.exceptions import PermissionDenied


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(
            models.Q(organizer=user) |
            models.Q(participants=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class MeetingMinutesViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingMinutesSerializer

    def get_queryset(self):
        user = self.request.user
        return MeetingMinutes.objects.filter(
            models.Q(meeting__organizer=user) |
            models.Q(meeting__participants=user)
        ).distinct()

    def perform_create(self, serializer):
        meeting = serializer.validated_data['meeting']
        user = self.request.user

        if not (
            user == meeting.organizer or
            meeting.participants.filter(id=user.id).exists()
        ):
            raise PermissionDenied("You are not part of this meeting.")

        serializer.save(author=user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            models.Q(minutes__meeting__organizer=user) |
            models.Q(minutes__meeting__participants=user)
        ).distinct()

    def perform_create(self, serializer):
        minutes = serializer.validated_data['minutes']
        meeting = minutes.meeting
        user = self.request.user

        if not (
            user == meeting.organizer or
            meeting.participants.filter(id=user.id).exists()
        ):
            raise PermissionDenied("You are not part of this meeting.")

        serializer.save()

    def get_serializer_context(self):
        return {'request': self.request}


