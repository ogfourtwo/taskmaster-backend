from .models import MeetingRole
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsMeetingManagerOrParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        meeting = obj.meeting
        user_roles = MeetingRole.objects.filter(meeting=meeting, user=user)

        if not user_roles.exists():
            return False

        role = user_roles.first().role
        if request.method in SAFE_METHODS:
            return role in ['manager', 'participant']
        else:
            return role == 'manager'
