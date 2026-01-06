from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Meeting, MeetingMinutes, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

class MeetingMinutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingMinutes
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['assigned_by']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        minutes = validated_data['minutes']
        meeting = minutes.meeting

        # 🚫 BLOCK task creation if meeting is done
        if meeting.status in ['completed', 'canceled']:
            raise serializers.ValidationError(
                "Cannot add tasks to a completed or canceled meeting."
            )

        # ✅ Set assigned_by safely
        validated_data['assigned_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        meeting = instance.minutes.meeting
    
        if meeting.status in ['completed', 'canceled']:
            raise serializers.ValidationError(
                "Cannot modify tasks from a completed or canceled meeting."
            )
    
        return super().update(instance, validated_data)
