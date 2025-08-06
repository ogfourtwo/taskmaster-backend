from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Meeting, MeetingMinutes, Task
from .serializers import UserSerializer, MeetingSerializer, MeetingMinutesSerializer, TaskSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import MeetingRole
from .serializers import MeetingRoleSerializer, AssignMeetingRoleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import IsMeetingManagerOrParticipant

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MeetingMinutesViewSet(viewsets.ModelViewSet):
    queryset = MeetingMinutes.objects.all()
    serializer_class = MeetingMinutesSerializer
    permission_classes = [IsAuthenticated, IsMeetingManagerOrParticipant]
    
    def get_queryset(self):
        user = self.request.user
        meetings = Meeting.objects.filter(roles__user=user)
        return MeetingMinutes.objects.filter(meeting__in=meetings)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsMeetingManagerOrParticipant]

    def get_queryset(self):
        user = self.request.user
        meetings = Meeting.objects.filter(roles__user=user)
        return Task.objects.filter(minutes__meeting__in=meetings)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(roles__user=user)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def roles(self, request, pk=None):
        meeting = self.get_object()
        roles = MeetingRole.objects.filter(meeting=meeting)
        return Response(MeetingRoleSerializer(roles, many=True).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assign_role(self, request, pk=None):
        meeting = self.get_object()
        current_role = MeetingRole.objects.filter(meeting=meeting, user=request.user).first()
        if not current_role or current_role.role != 'manager':
            return Response({'error': 'Only managers can assign roles'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AssignMeetingRoleSerializer(data=request.data)
        if serializer.is_valid():
            MeetingRole.objects.update_or_create(
                meeting=meeting,
                user=serializer.validated_data['user'],
                defaults={'role': serializer.validated_data['role']}
            )
            return Response({'message': 'Role assigned'})
        return Response(serializer.errors, status=400)